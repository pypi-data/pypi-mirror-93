// Copyright 2019 Global Phasing Ltd.
//
// convert MTZ to SF-mmCIF

#include <cstdio>
#include <cstdlib>            // for strtod
#include <iostream>           // for cout, cerr
#include <gemmi/mtz2cif.hpp>
#include <gemmi/gz.hpp>       // for MaybeGzipped
#include <gemmi/fstream.hpp>  // for Ofstream
#define GEMMI_PROG mtz2cif
#include "options.h"

namespace {

enum OptionIndex { Spec=4, PrintSpec, BlockName, EntryId, SkipEmpty,
                   NoComments, Wavelength, ValidateMerge, Trim };

const option::Descriptor Usage[] = {
  { NoOp, 0, "", "", Arg::None,
    "Usage:\n  " EXE_NAME " [options] MTZ_FILE [MTZ_FILE] CIF_FILE"
    "\nOptions:"},
  CommonUsage[Help],
  CommonUsage[Version],
  CommonUsage[Verbose],
  { Spec, 0, "", "spec", Arg::Required,
    "  --spec=FILE  \tColumn and format specification." },
  { PrintSpec, 0, "", "print-spec", Arg::None,
    "  --print-spec  \tPrint default spec and exit." },
  { BlockName, 0, "b", "block", Arg::Required,
    "  -b NAME, --block=NAME  \tmmCIF block name: data_NAME (default: mtz)." },
  { EntryId, 0, "", "id", Arg::Required,
    "  --id=ID  \tvalue for _entry.id (default: xxxx)." },
  { SkipEmpty, 0, "", "skip-empty", Arg::Optional,
    "  --skip-empty[=COLS]  \tSkip reflections with no values. If COLS are "
    "given, eg. 'I(+),I(-)', only values in those columns are checked." },
  { NoComments, 0, "", "no-comments", Arg::None,
    "  --no-comments  \tDo not write comments in the mmCIF file." },
  { Wavelength, 0, "", "wavelength", Arg::Float,
    "  --wavelength=LAMBDA  \tSet wavelengths (default: from input file)." },
  { ValidateMerge, 0, "", "validate-merge", Arg::None,
    "  --validate-merge  \tFor two MTZ files: validate the intensities match." },
  { Trim, 0, "", "trim", Arg::Int,
    "  --trim=N  \t(for testing) output only reflections -N <= h,k,l <=N." },
  { NoOp, 0, "", "", Arg::None,
    "\nOne or two MTZ files are taken as the input. If two files are given,"
    "\none must be merged and the other unmerged."
    "\nIf CIF_FILE is -, the output is printed to stdout."
    "\nIf spec is -, it is read from stdin."
    "\n\nLines in the spec file have format:"
    "\n  [FLAG] COLUMN TYPE TAG [FORMAT]"
    "\n or"
    "\n  $SPECIAL TAG"
    "\nfor example:"
    "\n  SIGF_native * SIGF_meas_au 12.5e"
    "\n  FREE I pdbx_r_free_flag 3.0f"
    "\n  $counter id"
    "\nFLAG (optional) is either ? or &:"
    "\n  ? = ignored if no column in the MTZ file has this name."
    "\n  & = ignored if the previous line was ignored."
    "\n  Example:"
    "\n      ? I    J intensity_meas"
    "\n      & SIGI Q intensity_sigma"
    "\nCOLUMN is MTZ column label. Columns H K L are added if not specified."
    "\n  Alternative labels can be separated with | (e.g. FREE|FreeR_flag)."
    "\nTYPE is used for checking the columm type, unless it is '*'."
    "\nTAG does not include category name, it is only the part after _refln."
    "\nFORMAT (optional) is printf-like floating-point format:"
    "\n - one of e, f, g with optional flag, width and precision"
    "\n - flag is one of + - # _; '_' stands for ' ', for example '_.4f'"
    "\n - since all numbers in MTZ are stored as float, the integer columns use"
    "\n   the same format as float. The format of _refln.status is ignored."
    "\n$SPECIAL is $counter, $dataset, $image, $. or $?, as appropriate for"
    "\n  _diffrn_refln.id, _diffrn_refln.diffrn_id, image number or null (./?)"
  },
  { 0, 0, 0, 0, 0, 0 }
};

} // anonymous namespace

int GEMMI_MAIN(int argc, char **argv) {
  OptParser p(EXE_NAME);
  p.simple_parse(argc, argv, Usage);
  if (p.options[PrintSpec]) {
    std::printf("                                for merged mtz\n");
    const char** lines = gemmi::MtzToCif::default_spec(/*for_merged=*/true);
    for (; *lines != nullptr; ++lines)
      std::printf("%s\n", *lines);
    std::printf("\n                             for unmerged mtz\n");
    lines = gemmi::MtzToCif::default_spec(/*for_merged=*/false);
    for (; *lines != nullptr; ++lines)
      std::printf("%s\n", *lines);
    return 0;
  }
  int nargs = p.nonOptionsCount();
  if (nargs != 2 && nargs != 3) {
    fprintf(stderr, "%s requires 2 or 3 arguments, got %d.", p.program_name, nargs);
    p.print_try_help_and_exit("");
  }
  bool verbose = p.options[Verbose];
  const char* mtz_paths[2];
  mtz_paths[0] = p.nonOption(0);
  mtz_paths[1] = (nargs == 3 ? p.nonOption(1) : nullptr);
  const char* cif_path = p.nonOption(nargs == 3 ? 2 : 1);
  std::unique_ptr<gemmi::Mtz> mtz[2];
  for (int i = 0; i < 2; ++i)
    if (mtz_paths[i]) {
      mtz[i].reset(new gemmi::Mtz);
      if (verbose) {
        std::fprintf(stderr, "Reading %s ...\n", mtz_paths[i]);
        mtz[i]->warnings = stderr;
      }
      try {
        mtz[i]->read_input(gemmi::MaybeGzipped(mtz_paths[i]), true);
      } catch (std::runtime_error& e) {
        std::fprintf(stderr, "ERROR reading %s: %s\n", mtz_paths[i], e.what());
        return 1;
      }
    }

  if (verbose)
    std::fprintf(stderr, "Writing %s ...\n", cif_path);

  gemmi::MtzToCif mtz_to_cif;

  try {
    if (p.options[Spec]) {
      char buf[256];
      const char* spec_path = p.options[Spec].arg;
      gemmi::fileptr_t f_spec = gemmi::file_open_or(spec_path, "r", stdin);
      while (fgets(buf, sizeof(buf), f_spec.get()) != NULL) {
        const char* start = gemmi::skip_blank(buf);
        if (*start != '\0' && *start != '\r' && *start != '\n' && *start != '#')
          mtz_to_cif.spec_lines.emplace_back(start);
      }
    }
  } catch (std::runtime_error& e) {
    std::fprintf(stderr, "Problem in translation spec: %s\n", e.what());
    return 2;
  }

  mtz_to_cif.mtz_path = mtz_paths[0];
  if (mtz_paths[1]) {
    mtz_to_cif.mtz_path += " and ";
    mtz_to_cif.mtz_path += mtz_paths[1];
  }
  mtz_to_cif.with_comments = !p.options[NoComments];
  if (p.options[SkipEmpty]) {
    mtz_to_cif.skip_empty = true;
    if (p.options[SkipEmpty].arg)
      mtz_to_cif.skip_empty_cols = p.options[SkipEmpty].arg;
  }
  if (p.options[BlockName])
    mtz_to_cif.block_name = p.options[BlockName].arg;
  if (p.options[EntryId])
    mtz_to_cif.entry_id = p.options[EntryId].arg;
  if (p.options[Wavelength])
    mtz_to_cif.wavelength = std::strtod(p.options[Wavelength].arg, nullptr);
  if (p.options[ValidateMerge] && nargs == 3) {
    try {
      gemmi::validate_merged_intensities(*mtz[0], *mtz[1], std::cerr);
    } catch (std::runtime_error& e) {
      fprintf(stderr, "Intensity merging not validated: %s\n", e.what());
    }
  }
  if (p.options[Trim])
    mtz_to_cif.trim = std::atoi(p.options[Trim].arg);
  try {
    gemmi::Ofstream os(cif_path, &std::cout);
    mtz[0]->switch_to_original_hkl();
    if (mtz[1])
      mtz[1]->switch_to_original_hkl();
    mtz_to_cif.write_cif(*mtz[0], mtz[1].get(), os.ref());
  } catch (std::runtime_error& e) {
    std::fprintf(stderr, "ERROR writing %s: %s\n", cif_path, e.what());
    return 3;
  }
  return 0;
}

// vim:sw=2:ts=2:et:path^=../include,../third_party
