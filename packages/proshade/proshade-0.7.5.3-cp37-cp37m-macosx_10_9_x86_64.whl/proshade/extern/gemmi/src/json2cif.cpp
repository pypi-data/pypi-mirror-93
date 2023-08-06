// Copyright 2017 Global Phasing Ltd.

#include "gemmi/gzread.hpp"   // for read_cif_gz
#include "gemmi/to_cif.hpp"   // for JsonWriter
#include "gemmi/fstream.hpp"  // for Ofstream

#include <cstring>
#include <iostream>
#include <map>

#define GEMMI_PROG json2cif
#include "options.h"
#include "cifmod.h"  // for apply_cif_doc_modifications, ...

namespace {

enum OptionIndex { PdbxStyle=AfterCifModOptions, Cif2Cif };

const option::Descriptor Usage[] = {
  { NoOp, 0, "", "", Arg::None,
    "Usage:"
    "\n " EXE_NAME " [options] INPUT_FILE OUTPUT_FILE"
    "\n\nConvert mmJSON to mmCIF."
    "\n\nOptions:" },
  CommonUsage[Help],
  CommonUsage[Version],
  CommonUsage[Verbose],

  { PdbxStyle, 0, "", "pdbx-style", Arg::None,
    "  --pdbx-style  \tSimilar styling (formatting) as in wwPDB." },
  { Cif2Cif, 0, "", "cif2cif", Arg::None,
    "  --cif2cif  \tRead CIF not JSON." },
  CifModUsage[SkipCat],
  CifModUsage[SortCif],

  { NoOp, 0, "", "", Arg::None,
    "\nWhen output file is -, write to standard output." },
  { 0, 0, 0, 0, 0, 0 }
};

} // anonymous namespace

int GEMMI_MAIN(int argc, char **argv) {
  std::ios_base::sync_with_stdio(false);
  OptParser p(EXE_NAME);
  p.simple_parse(argc, argv, Usage);
  p.require_positional_args(2);

  const char* input = p.nonOption(0);
  const char* output = p.nonOption(1);
  namespace cif = gemmi::cif;
  auto style = p.options[PdbxStyle] ? cif::Style::Pdbx
                                    : cif::Style::PreferPairs;

  if (p.options[Verbose])
    std::cerr << "Transcribing " << input << " to cif ..." << std::endl;
  try {
    cif::Document doc = p.options[Cif2Cif] ? gemmi::read_cif_gz(input)
                                           : gemmi::read_mmjson_gz(input);
    apply_cif_doc_modifications(doc, p.options);
    gemmi::Ofstream os(output, &std::cout);
    write_cif_to_stream(os.ref(), doc, style);
  } catch (std::runtime_error& e) {
    std::cerr << "ERROR: " << e.what() << std::endl;
    return 2;
  } catch (std::invalid_argument& e) {
    std::cerr << "ERROR: " << e.what() << std::endl;
    return 3;
  }
  if (p.options[Verbose])
    std::cerr << "Done." << std::endl;
  return 0;
}

// vim:sw=2:ts=2:et:path^=../include,../third_party
