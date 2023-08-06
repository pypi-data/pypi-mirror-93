/*! \file pyProSHADE.cpp
    \brief This file contains the PyBind11 bindings for the ProSHADE_data class.
    
    This file provides the bindings for the ProSHADE_data class members and functions. It also defines several python specific functions (written as C++ lambda functions) which allow direct access
    to the computed results as numpy.ndarrays, while making sure the memory is released correctly for such cross-language shared variables.
    
    Copyright by Michal Tykac and individual contributors. All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
    1) Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    2) Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    3) Neither the name of Michal Tykac nor the names of this code's contributors may be used to endorse or promote products derived from this software without specific prior written permission.

    This software is provided by the copyright holder and contributors "as is" and any express or implied warranties, including, but not limitted to, the implied warranties of merchantibility and fitness for a particular purpose are disclaimed. In no event shall the copyright owner or the contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limitted to, procurement of substitute goods or services, loss of use, data or profits, or business interuption) however caused and on any theory of liability, whether in contract, strict liability or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
 
    \author    Michal Tykac
    \author    Garib N. Murshudov
    \version   0.7.5.2
    \date      JAN 2021
 */

//==================================================== Include PyBind11 header
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

//==================================================== Add the ProSHADE_settings and ProSHADE_run classes to the PyBind11 module
void add_dataClass ( pybind11::module& pyProSHADE )
{
    //================================================ Export the ProSHADE_settings class
    pybind11::class_ < ProSHADE_internal_data::ProSHADE_data > ( pyProSHADE, "ProSHADE_data" )
        
        //============================================ Constructors (destructors do not need wrappers???)
        .def                                          ( pybind11::init < ProSHADE_settings* > ( ), pybind11::arg ( "settings" ) )
        .def                                          ( pybind11::init ( [] ( ProSHADE_settings* settings, std::string strName, pybind11::array_t < float, pybind11::array::c_style | pybind11::array::forcecast > mapData, proshade_single xDmSz, proshade_single yDmSz, proshade_single zDmSz, proshade_unsign xDmInd, proshade_unsign yDmInd, proshade_unsign zDmInd, proshade_signed xFr, proshade_signed yFr, proshade_signed zFr, proshade_signed xT, proshade_signed yT, proshade_signed zT,  proshade_unsign inputO )
                                                      {
                                                        //== Find the array size
                                                        pybind11::buffer_info buf = mapData.request();
                                                        proshade_unsign len = buf.size;
            
                                                        //== Allocate memory
                                                        double* npVals = new double[static_cast<proshade_unsign> ( len )];
                                                        ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
            
                                                        //== Copy from numpy to ProSHADE (I do not want to be directly changing the python memory, that screams trouble)
                                                        if ( buf.ndim == 1 )
                                                        {
                                                            for ( proshade_unsign iter = 0; iter < len; iter++ ) { npVals[iter] = static_cast < double > ( mapData.at(iter) ); }
                                                        }
                                                        else if ( buf.ndim == 3 )
                                                        {
                                                            float* dataPtr = reinterpret_cast < float* > ( buf.ptr );
                                                            for ( proshade_unsign xIt = 0; xIt < static_cast<proshade_unsign> ( buf.shape.at(0) ); xIt++ )
                                                            {
                                                                for ( proshade_unsign yIt = 0; yIt < static_cast<proshade_unsign> ( buf.shape.at(1) ); yIt++ )
                                                                {
                                                                    for ( proshade_unsign zIt = 0; zIt < static_cast<proshade_unsign> ( buf.shape.at(2) ); zIt++ )
                                                                    {
                                                                        npVals[zIt + buf.shape.at(2) * ( yIt + buf.shape.at(1) * xIt )] = static_cast < double > ( dataPtr[zIt + buf.shape.at(2) * ( yIt + buf.shape.at(1) * xIt )] );
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        else
                                                        {
                                                            std::cerr << "!!! ProSHADE PYTHON MODULE ERROR !!! The ProSHADE_data class constructor ( ProSHADE_settings, str, numpy.ndarray, float, float, float, ... ) only supports the third argument input array in the 1D or 3D numpy.ndarray format. The supplied array has " << buf.ndim << " dims. Terminating..." << std::endl;
                                                            exit ( EXIT_FAILURE );
                                                        }
            
                                                        //== Call the ProSHADE_data constructor
                                                        return new ProSHADE_internal_data::ProSHADE_data ( settings,
                                                                                                           strName,
                                                                                                           npVals,
                                                                                                           static_cast<int> ( len ),
                                                                                                           xDmSz,
                                                                                                           yDmSz,
                                                                                                           zDmSz,
                                                                                                           xDmInd,
                                                                                                           yDmInd,
                                                                                                           zDmInd,
                                                                                                           xFr,
                                                                                                           yFr,
                                                                                                           zFr,
                                                                                                           xT,
                                                                                                           yT,
                                                                                                           zT,
                                                                                                           inputO );
                                                      } ) )
    
        //============================================ Data I/O functions
        .def                                          ( "readInStructure",  &ProSHADE_internal_data::ProSHADE_data::readInStructure,    "This function initialises the basic ProSHADE_data variables and reads in a single structure.", pybind11::arg ( "fname" ), pybind11::arg ( "inputO" ), pybind11::arg ( "settings" ) )
        .def                                          ( "writeMap",         &ProSHADE_internal_data::ProSHADE_data::writeMap,           "Function for writing out the internal structure representation in MRC MAP format.",            pybind11::arg ( "fname" ), pybind11::arg ( "title" ) = "Created by ProSHADE and written by GEMMI", pybind11::arg ( "mode" ) = 2 )
        .def                                          ( "writePdb",         &ProSHADE_internal_data::ProSHADE_data::writePdb,           "This function writes out the PDB formatted file coresponding to the structure.",               pybind11::arg ( "fname" ), pybind11::arg ( "euA" ) = 0.0, pybind11::arg ( "euB" ) = 0.0, pybind11::arg ( "euG" ) = 0.0, pybind11::arg ( "trsX" ) = 0.0, pybind11::arg ( "trsY" ) = 0.0, pybind11::arg ( "trsZ" ) = 0.0, pybind11::arg ( "firstModel" ) = true )
        .def                                          ( "getMap",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self ) -> pybind11::array_t < proshade_double >
                                                        {
                                                            //== Copy the values
                                                            pybind11::array_t < proshade_double > retArr = pybind11::array_t < proshade_double > ( { self.xDimIndices, self.yDimIndices, self.zDimIndices },  // Shape
                                                                                                                                                   { self.yDimIndices * self.zDimIndices * sizeof(proshade_double),
                                                                                                                                                     self.zDimIndices * sizeof(proshade_double),
                                                                                                                                                     sizeof(proshade_double) },  // C-stype strides
                                                                                                                                                   self.internalMap );           // Data

                                                            //== Done
                                                            return ( retArr );
                                                        } )
    
        //============================================ Data processing functions
        .def                                          ( "processInternalMap",    &ProSHADE_internal_data::ProSHADE_data::processInternalMap,    "This function simply clusters several map manipulating functions which should be called together. These include centering, phase removal, normalisation, adding extra space, etc.", pybind11::arg ( "settings" ) )
        .def                                          ( "invertMirrorMap",       &ProSHADE_internal_data::ProSHADE_data::invertMirrorMap,       "Function for inverting the map to its mirror image.", pybind11::arg ( "settings" ) )
        .def                                          ( "normaliseMap",          &ProSHADE_internal_data::ProSHADE_data::normaliseMap,          "Function for normalising the map values to mean 0 and sd 1.", pybind11::arg ( "settings" ) )
        .def                                          ( "maskMap",               &ProSHADE_internal_data::ProSHADE_data::maskMap,               "Function for computing the map mask using blurring and X IQRs from median.", pybind11::arg ( "settings" ) )
        .def                                          ( "reSampleMap",           &ProSHADE_internal_data::ProSHADE_data::reSampleMap,           "This function changes the internal map sampling to conform to particular resolution value.", pybind11::arg ( "settings" ) )
        .def                                          ( "centreMapOnCOM",        &ProSHADE_internal_data::ProSHADE_data::centreMapOnCOM,        "This function shits the map so that its COM is in the centre of the map.", pybind11::arg ( "settings" ) )
        .def                                          ( "addExtraSpace",         &ProSHADE_internal_data::ProSHADE_data::addExtraSpace,         "This function increases the size of the map so that it can add empty space around it.", pybind11::arg ( "settings" ) )
        .def                                          ( "removePhaseInormation", &ProSHADE_internal_data::ProSHADE_data::removePhaseInormation, "This function removes phase from the map, effectively converting it to Patterson map.", pybind11::arg ( "settings" ) )
        .def                                          ( "getReBoxBoundaries",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self,ProSHADE_settings* settings ) -> pybind11::array_t < proshade_signed >
                                                        {
                                                            //== Allocate output memory
                                                            proshade_signed* retVals = new proshade_signed[6];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( retVals, __FILE__, __LINE__, __func__ );
            
                                                            //== If same bounds as first one are required, test if possible and return these instead
                                                            if ( settings->useSameBounds && ( self.inputOrder != 0 ) )
                                                            {
                                                                for ( proshade_unsign iter = 0; iter < 6; iter++ ) { retVals[iter] = settings->forceBounds[iter]; }
                                                            }
                                                            //== In this case, bounds need to be found de novo
                                                            else
                                                            {
                                                                //== Find the non-zero bounds
                                                                ProSHADE_internal_mapManip::getNonZeroBounds  ( self.internalMap, self.xDimIndices, self.yDimIndices, self.zDimIndices,
                                                                                                                self.xDimSize, self.yDimSize, self.zDimSize, retVals );
                                                                
                                                                //== Add the extra space
                                                                ProSHADE_internal_mapManip::addExtraBoundSpace ( self.xDimIndices, self.yDimIndices, self.zDimIndices,
                                                                                                                 self.xDimSize, self.yDimSize, self.zDimSize, retVals, settings->boundsExtraSpace );
                                                                
                                                                //== Beautify boundaries
                                                                ProSHADE_internal_mapManip::beautifyBoundaries ( retVals, self.xDimIndices, self.yDimIndices, self.zDimIndices, settings->boundsSimilarityThreshold, settings->verbose );
                                                                
                                                                //== If need be, save boundaries to be used for all other structure
                                                                if ( settings->useSameBounds && ( self.inputOrder == 0 ) ) { for ( proshade_unsign iter = 0; iter < 6; iter++ ) { settings->forceBounds[iter] = retVals[iter]; } }
                                                            }

                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleReBox2 ( retVals, []( void *f ) { proshade_signed* foo = reinterpret_cast< proshade_signed* > ( f ); delete foo; } );

                                                            //== Copy the value
                                                            pybind11::array_t < proshade_signed > retArr = pybind11::array_t < proshade_signed > ( { 6 },                         // Shape
                                                                                                                                                   { sizeof(proshade_signed) },   // C-stype strides
                                                                                                                                                   retVals,                       // Data
                                                                                                                                                   pyCapsuleReBox2 );             // Capsule

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function finds the boundaries enclosing positive map values and adds some extra space." )
        .def                                          ( "createNewMapFromBounds",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, pybind11::array_t < proshade_signed > bounds, ProSHADE_internal_data::ProSHADE_data* newStr, ProSHADE_settings* settings )
                                                        {
                                                            //== Allocate memory for bounds copy
                                                            proshade_signed* newBounds = new proshade_signed[6];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( newBounds, __FILE__, __LINE__, __func__ );
            
                                                            //== Copy to the pointer
                                                            for ( proshade_unsign iter = 0; iter < 6; iter++ ) { newBounds[iter] = bounds.at(iter); }
            
                                                            //== Run C++ function
                                                            self.createNewMapFromBounds ( settings, newStr, newBounds );

                                                            //== Done
                                                            return ;
                                                        }, "This function creates a new structure from the calling structure and new bounds values." )
    
        //============================================ Data sphere mapping functions
        .def                                          ( "mapToSpheres", &ProSHADE_internal_data::ProSHADE_data::mapToSpheres, "This function converts the internal map onto a set of concentric spheres.", pybind11::arg ( "settings" ) )
        .def                                          ( "getSpherePositions", &ProSHADE_internal_data::ProSHADE_data::getSpherePositions, "This function determines the sphere positions (radii) for sphere mapping.", pybind11::arg ( "settings" ) )
        .def                                          ( "computeSphericalHarmonics", &ProSHADE_internal_data::ProSHADE_data::computeSphericalHarmonics, "This function computes the spherical harmonics decomposition for the whole structure.", pybind11::arg ( "settings" ) )
    
        //============================================ Accessor functions
        .def                                          ( "getXDimSize", &ProSHADE_internal_data::ProSHADE_data::getXDimSize, "This function allows access to the map size in angstroms along the X axis." )
        .def                                          ( "getYDimSize", &ProSHADE_internal_data::ProSHADE_data::getYDimSize, "This function allows access to the map size in angstroms along the Y axis." )
        .def                                          ( "getZDimSize", &ProSHADE_internal_data::ProSHADE_data::getZDimSize, "This function allows access to the map size in angstroms along the Z axis." )
        .def                                          ( "getXDim",     &ProSHADE_internal_data::ProSHADE_data::getXDim,     "This function allows access to the map size in indices along the X axis."   )
        .def                                          ( "getYDim",     &ProSHADE_internal_data::ProSHADE_data::getYDim,     "This function allows access to the map size in indices along the Y axis."   )
        .def                                          ( "getZDim",     &ProSHADE_internal_data::ProSHADE_data::getZDim,     "This function allows access to the map size in indices along the Z axis."   )
    
        //============================================ Symmetry related functions
        .def                                          ( "computeRotationFunction", &ProSHADE_internal_data::ProSHADE_data::computeRotationFunction, "This function computes the self-rotation function for this structure and stores it internally in the ProSHADE_data object.", pybind11::arg ( "settings" ) )
        .def                                          ( "detectSymmetryInStructure",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings )
                                                        {
                                                            //== Call the appropriate C++ function
                                                            if ( settings->usePeakSearchInRotationFunctionSpace )
                                                            {
                                                                //== Detect point groups in the angle-axis space
                                                                self.detectSymmetryFromAngleAxisSpace ( settings, &settings->detectedSymmetry, &settings->allDetectedCAxes );
                                                            }
                                                            else
                                                            {
                                                                //== Detect symmetry using the peak detection in rotation function space
                                                                self.detectSymmetryInStructure ( settings, &settings->detectedSymmetry, &settings->allDetectedCAxes );
                                                            }
                                                        }, "This function runs the symmetry detection algorithms on this structure and saves the results in the settings object.", pybind11::arg ( "settings" ) )
        .def                                          ( "getRecommendedSymmetryType", &ProSHADE_internal_data::ProSHADE_data::getRecommendedSymmetryType, "This function simply returns the detected recommended symmetry type.", pybind11::arg ( "settings" ) )
        .def                                          ( "getRecommendedSymmetryFold", &ProSHADE_internal_data::ProSHADE_data::getRecommendedSymmetryFold, "This function simply returns the detected recommended symmetry fold.", pybind11::arg ( "settings" ) )
        .def                                          ( "getRecommendedSymmetryAxes",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings ) -> pybind11::array_t < float >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            float* npVals = new float[static_cast<unsigned int> ( settings->detectedSymmetry.size() * 6 )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
    
                                                            //== Copy values
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( settings->detectedSymmetry.size() ); iter++ ) { for ( proshade_unsign it = 0; it < 6; it++ ) { npVals[(iter*6)+it] = settings->detectedSymmetry.at(iter)[it]; } }
    
                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleStrRecSym ( npVals, []( void *f ) { float* foo = reinterpret_cast< float* > ( f ); delete foo; } );

                                                            //== Copy the value
                                                            pybind11::array_t < float > retArr = pybind11::array_t<float> ( { static_cast<int> ( settings->detectedSymmetry.size() ), static_cast<int> ( 6 ) },  // Shape
                                                                                                                            { 6 * sizeof(float), sizeof(float) },                          // C-stype strides
                                                                                                                            npVals,                                                        // Data
                                                                                                                            pyCapsuleStrRecSym );                                          // Capsule

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns the recommended symmetry axes as a 2D numpy array." )
        .def                                          ( "getAllCSyms",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings ) -> pybind11::array_t < float >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            float* npVals = new float[static_cast<unsigned int> ( settings->allDetectedCAxes.size() * 6 )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
        
                                                            //== Copy values
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( settings->allDetectedCAxes.size() ); iter++ ) { for ( proshade_unsign it = 0; it < 6; it++ ) { npVals[(iter*6)+it] = settings->allDetectedCAxes.at(iter).at(it); } }
        
                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleStrSymList ( npVals, []( void *f ) { float* foo = reinterpret_cast< float* > ( f ); delete foo; } );

                                                            //== Copy the value
                                                            pybind11::array_t < float > retArr = pybind11::array_t<float> ( { static_cast<int> ( settings->allDetectedCAxes.size() ), 6 },  // Shape
                                                                                                                            { 6 * sizeof(float), sizeof(float) },                           // C-stype strides
                                                                                                                            npVals,                                                         // Data
                                                                                                                            pyCapsuleStrSymList );                                          // Capsule

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns all symmetry axes as a 2D numpy array." )
        .def                                          ( "getNonCSymmetryAxesIndices",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings ) -> pybind11::dict
                                                        {
                                                            //== Initialise local variables
                                                            pybind11::dict retDict;
                                                            pybind11::list dList, tList, oList, iList;
            
                                                            //== Fill in the D list
                                                            for ( proshade_unsign dIt = 0; dIt < static_cast<proshade_unsign> ( settings->allDetectedDAxes.size() ); dIt++ )
                                                            {
                                                                pybind11::list memList;
                                                                for ( proshade_unsign memIt = 0; memIt < static_cast<proshade_unsign> ( settings->allDetectedDAxes.at(dIt).size() ); memIt++ )
                                                                {
                                                                    memList.append ( settings->allDetectedDAxes.at(dIt).at(memIt) );
                                                                }
                                                                dList.append ( memList );
                                                            }
            
                                                            //== Fill in the T list
                                                            for ( proshade_unsign tIt = 0; tIt < static_cast<proshade_unsign> ( settings->allDetectedTAxes.size() ); tIt++ )
                                                            {
                                                                tList.append ( settings->allDetectedTAxes.at ( tIt ) );
                                                            }
            
                                                            //== Fill in the O list
                                                            for ( proshade_unsign oIt = 0; oIt < static_cast<proshade_unsign> ( settings->allDetectedOAxes.size() ); oIt++ )
                                                            {
                                                                oList.append ( settings->allDetectedOAxes.at ( oIt ) );
                                                            }
            
                                                            //== Fill in the T list
                                                            for ( proshade_unsign iIt = 0; iIt < static_cast<proshade_unsign> ( settings->allDetectedIAxes.size() ); iIt++ )
                                                            {
                                                                iList.append ( settings->allDetectedIAxes.at ( iIt ) );
                                                            }
            
                                                            //== Save the lists to the dict
                                                            retDict[ pybind11::handle ( pybind11::str ( "D" ).ptr ( ) ) ] = dList;
                                                            retDict[ pybind11::handle ( pybind11::str ( "T" ).ptr ( ) ) ] = tList;
                                                            retDict[ pybind11::handle ( pybind11::str ( "O" ).ptr ( ) ) ] = oList;
                                                            retDict[ pybind11::handle ( pybind11::str ( "I" ).ptr ( ) ) ] = iList;

                                                            //== Done
                                                            return ( retDict );
                                                        }, "This function returns array of non-C axes indices." )
        .def                                          ( "getAllGroupElements",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings, pybind11::array_t < int > axList, std::string groupType, proshade_double matrixTolerance ) -> pybind11::list
                                                        {
                                                            //== Sanity check
                                                            pybind11::buffer_info buf = axList.request();
                                                            if ( buf.ndim != 1 ) { std::cerr << "!!! ProSHADE PYTHON MODULE ERROR !!! The second argument to getAllGroupElements() must be a 1D numpy array stating the indices of the axes forming the group!" << std::endl; exit ( EXIT_FAILURE ); }
                                                            
                                                            //== Convert to vector of unsigns
                                                            std::vector< proshade_unsign > axesList;
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( axList.size() ); iter++ ) { ProSHADE_internal_misc::addToUnsignVector ( &axesList, axList.at(iter) ); }
            
                                                            //== Get the results
                                                            std::vector < std::vector< proshade_double > > vals = self.getAllGroupElements ( settings, axesList, groupType, matrixTolerance );
    
                                                            //== Initialise return variable
                                                            pybind11::list retList;
            
                                                            //== Copy values
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( vals.size() ); iter++ )
                                                            {
                                                                //== Allocate memory for the numpy values
                                                                float* npVals = new float[static_cast<unsigned int> ( 9 )];
                                                                ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
                                                                
                                                                //== Copy values to memory
                                                                for ( proshade_unsign it = 0; it < 9; it++ ) { npVals[it] = vals.at(iter).at(it); }
    
                                                                //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                                pybind11::capsule pyCapsuleGrpEl ( npVals, []( void *f ) { float* foo = reinterpret_cast< float* > ( f ); delete foo; } );

                                                                //== Copy the value
                                                                pybind11::array_t < float > retArr = pybind11::array_t<float> ( { 3, 3 },                                      // Shape
                                                                                                                                { 3 * sizeof(float), sizeof(float) },          // C-stype strides
                                                                                                                                npVals,                                        // Data
                                                                                                                                pyCapsuleGrpEl );                              // Capsule
                                                                
                                                                //== Save matrix
                                                                retList.append ( retArr );
                                                            }

                                                            //== Done
                                                            return ( retList );
                                                        }, "This function returns the group elements as rotation matrices of any point group described by the detected axes.", pybind11::arg ( "settings" ), pybind11::arg ( "axList" ), pybind11::arg ( "groupType" ) = "", pybind11::arg( "matrixTolerance" ) = 0.05 )
    
        //============================================ Overlay related functions
        .def                                          ( "getOverlayRotationFunction", &ProSHADE_internal_data::ProSHADE_data::getOverlayRotationFunction, "This function computes the overlay rotation function (i.e. the correlation function in SO(3) space).", pybind11::arg ( "settings" ), pybind11::arg ( "obj2" ) )
        .def                                          ( "getBestRotationMapPeaksEulerAngles",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings ) -> pybind11::array_t < float >
                                                        {
                                                            //== Get values
                                                            std::vector< proshade_double > vals = self.getBestRotationMapPeaksEulerAngles ( settings );
            
                                                            //== Allocate memory for the numpy values
                                                            float* npVals = new float[static_cast<unsigned int> (vals.size())];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );

                                                            //== Copy values
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( vals.size() ); iter++ ) { npVals[iter] = vals.at(iter); }

                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleEuPeak ( npVals, []( void *f ) { float* foo = reinterpret_cast< float* > ( f ); delete foo; } );

                                                            //== Copy the value
                                                            pybind11::array_t < float > retArr = pybind11::array_t<float> ( { static_cast<unsigned int> (vals.size()) },  // Shape
                                                                                                                            { sizeof(float) },                            // C-stype strides
                                                                                                                            npVals,                                       // Data
                                                                                                                            pyCapsuleEuPeak );                            // Capsule (C++ destructor, basically)

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns a vector of three floats, the three Euler angles of the best peak in the rotation map.", pybind11::arg ( "settings" ) )
        .def                                          ( "getBestRotationMapPeaksRotationMatrix",
                                                    [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_settings* settings ) -> pybind11::array_t < proshade_double >
                                                    {
                                                        //== Get values
                                                        std::vector< proshade_double > vals = self.getBestRotationMapPeaksEulerAngles ( settings );
            
                                                        //== Convert Euler ZXZ to matrix
                                                        proshade_double* retMat = new proshade_double[9];
                                                        ProSHADE_internal_misc::checkMemoryAllocation ( retMat, __FILE__, __LINE__, __func__ );
                                                        ProSHADE_internal_maths::getRotationMatrixFromEulerZXZAngles ( vals.at(0), vals.at(1), vals.at(2), retMat );

                                                        //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                        pybind11::capsule pyCapsuleRMPeak ( retMat, []( void *f ) { proshade_double* foo = reinterpret_cast< proshade_double* > ( f ); delete foo; } );

                                                        //== Copy the value
                                                        pybind11::array_t < proshade_double > retArr = pybind11::array_t<proshade_double> ( { 3, 3 },                                                 // Shape
                                                                                                                                            { 3 * sizeof(proshade_double), sizeof(proshade_double) }, // C-stype strides
                                                                                                                                            retMat,                                                   // Data
                                                                                                                                            pyCapsuleRMPeak );                                        // Capsule

                                                        //== Done
                                                        return ( retArr );
                                                    }, "This function returns a rotation matrix representing the best peak in the rotation map.", pybind11::arg ( "settings" ) )
        .def                                          ( "rotateMap", &ProSHADE_internal_data::ProSHADE_data::rotateMap, "This function rotates a map based on the given Euler angles.", pybind11::arg ( "settings" ), pybind11::arg ( "eulerAlpha" ), pybind11::arg ( "eulerBeta" ), pybind11::arg ( "eulerGamma" ) )
        .def                                          ( "zeroPaddToDims", &ProSHADE_internal_data::ProSHADE_data::zeroPaddToDims, "This function changes the size of a structure to fit the supplied new limits.", pybind11::arg ( "xDimMax" ), pybind11::arg ( "yDimMax" ), pybind11::arg ( "zDimMax" ) )
        .def                                          ( "computeTranslationMap", &ProSHADE_internal_data::ProSHADE_data::computeTranslationMap, "This function does the computation of the translation map and saves results internally.", pybind11::arg ( "staticStructure" ) )
        .def                                          ( "getOverlayTranslations",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, ProSHADE_internal_data::ProSHADE_data* staticStructure , proshade_double eulA, proshade_double eulB, proshade_double eulG) -> pybind11::dict
                                                        {
                                                            //== Get values
                                                            std::vector< proshade_double > vals = self.getBestTranslationMapPeaksAngstrom ( staticStructure, eulA, eulB, eulG );

                                                            //== Initialise variables
                                                            pybind11::dict retDict;
                                                            pybind11::list rotCen, toOverlay;
            
                                                            //== Copy values
                                                            rotCen.append ( self.originalPdbRotCenX );
                                                            rotCen.append ( self.originalPdbRotCenY );
                                                            rotCen.append ( self.originalPdbRotCenZ );

                                                            toOverlay.append ( self.originalPdbTransX );
                                                            toOverlay.append ( self.originalPdbTransY );
                                                            toOverlay.append ( self.originalPdbTransZ );

                                                            //== Save results to return dict
                                                            retDict[ pybind11::handle ( pybind11::str ( "centreOfRotation" ).ptr ( ) ) ] = rotCen;
                                                            retDict[ pybind11::handle ( pybind11::str ( "rotCenToOverlay" ).ptr ( ) ) ] = toOverlay;

                                                            //== Done
                                                            return ( retDict );
                                                        }, "This function returns the vector from optimal rotation centre to origin and the optimal overlay translation vector. These two vectors allow overlaying the inputs (see documentation for details on how the two vectors should be used).", pybind11::arg ( "staticStructure" ), pybind11::arg ( "eulA" ), pybind11::arg ( "eulB" ), pybind11::arg ( "eulG" ) )
        .def                                          ( "translateMap", &ProSHADE_internal_data::ProSHADE_data::translateMap, "This function translates the map by a given number of Angstroms along the three axes. Please note the translation happens firstly to the whole map box and only the translation remainder that cannot be achieved by moving the box will be corrected for using reciprocal space translation within the box.", pybind11::arg ( "settings" ), pybind11::arg ( "trsX" ), pybind11::arg ( "trsY" ), pybind11::arg ( "trsZ" ) )

        //============================================ Internal arrays access functions
        .def                                          ( "findSHIndex",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, proshade_signed shell, proshade_signed band, proshade_signed order ) -> proshade_signed
                                                        {
                                                            //== Get value
                                                            proshade_signed index = seanindex ( order, band, self.spheres[shell]->getLocalBandwidth() );
            
                                                            //== Done
                                                            return ( index );
                                                        }, "This function finds the correct index for given shell, band and order in the spherical harmonics array. Please note that the order is expected in range -band <= 0 <- band and NOT from 0 to ( 2 * band ) + 1." )
        .def                                          ( "getSphericalHarmonics",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self ) -> pybind11::array_t < std::complex<proshade_double> >
                                                       {
                                                            //== Allocate memory for the numpy values
                                                            std::complex<proshade_double>* npVals = new std::complex<proshade_double>[static_cast<proshade_unsign> ( self.noSpheres * pow( self.maxShellBand, 2.0 ) )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
            
                                                            //== Fill with zeroes as the matrix will be sparse
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( self.noSpheres * pow( self.maxShellBand, 2.0 ) ); iter++ ) { npVals[iter].real ( 0.0 );  npVals[iter].imag ( 0.0 ); }
                                                            
                                                            //== Initialise variables
                                                            proshade_signed pyPosSH;
                                                            proshade_signed pyPos;
            
                                                            //== Copy data to new memory
                                                            for ( proshade_signed shIt = 0; shIt < static_cast<proshade_signed> ( self.noSpheres ); shIt++ )
                                                            {
                                                                for ( proshade_signed bnd = 0; bnd < static_cast<proshade_signed> ( self.spheres[shIt]->getLocalBandwidth() ); bnd++ )
                                                                {
                                                                    for ( proshade_signed order = -bnd; order <= bnd; order++ )
                                                                    {
                                                                        pyPosSH = ( shIt * pow( self.maxShellBand, 2.0 ) );
                                                                        pyPos   = seanindex ( order, bnd, self.spheres[shIt]->getLocalBandwidth() );
                                                                        npVals[pyPosSH+pyPos].real ( self.sphericalHarmonics[shIt][pyPos][0] );
                                                                        npVals[pyPosSH+pyPos].imag ( self.sphericalHarmonics[shIt][pyPos][1] );
                                                                    }
                                                                }
                                                            }

                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleSHs ( npVals, []( void *f ) { std::complex<proshade_double>* foo = reinterpret_cast< std::complex<proshade_double>* > ( f ); delete foo; } );

                                                            //== Copy the value
                                                            pybind11::array_t < std::complex<proshade_double> > retArr = pybind11::array_t < std::complex<proshade_double > > (
                                                                { static_cast<int> ( self.noSpheres ), static_cast<int> ( pow ( self.maxShellBand, 2.0  ) ) },
                                                                { sizeof ( std::complex < proshade_double > ) * static_cast<int> ( pow ( self.maxShellBand, 2.0  ) ), sizeof ( std::complex < proshade_double > ) },
                                                                npVals,
                                                                pyCapsuleSHs );
                
                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns a 2D numpy array of complex numbers representing the spherical harmonics computed for the structure. The first dimension of the array is the spheres (i.e. each sphere has its own array) and the second dimension is the band and order combination as given by the findSHIndex() function. Please note that while each sphere can have different number of spherical harmonics coefficients (depending on the settings.progressiveSphereMapping value), this array uses maxShellBand**2 values to make sure the length are equal for all spheres. To avoid issues, please use the findSHIndex() to correctly find the index of a particular shell, band, order combination." )
        .def                                          ( "getEMatrix",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self ) -> pybind11::array_t < std::complex < proshade_double > >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            std::complex<proshade_double>* npVals = new std::complex < proshade_double >[static_cast<proshade_unsign> ( self.maxShellBand * ( ( self.maxShellBand * 2 ) + 1 ) * ( ( self.maxShellBand * 2 ) + 1 ) )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
        
                                                            //== Allocate local variables
                                                            proshade_signed index = 0;
                                                                                                                                                                    
                                                            //== Fill with zeroes as the matrix will be sparse
                                                            for ( proshade_unsign iter = 0; iter < static_cast < proshade_unsign > ( self.maxShellBand * ( ( self.maxShellBand * 2 ) + 1 ) * ( ( self.maxShellBand * 2 ) + 1 ) ); iter++ ) { npVals[iter].real ( 0.0 );  npVals[iter].imag ( 0.0 ); }
        
                                                            //== Copy data to new memory
                                                            for ( proshade_signed bandIter = 0; bandIter < static_cast< proshade_signed > ( self.maxShellBand ); bandIter++ )
                                                            {
                                                                for ( proshade_unsign order1 = 0; order1 < ( ( bandIter * 2 ) + 1 ); order1++ )
                                                                {
                                                                    for ( proshade_unsign order2 = 0; order2 < ( ( bandIter * 2 ) + 1 ); order2++ )
                                                                    {
                                                                        index = order2 + ( ( self.maxShellBand * 2 ) + 1 ) * ( order1 + ( ( self.maxShellBand * 2 ) + 1 ) * bandIter );
                                                                        npVals[index].real ( self.eMatrices[bandIter][order1][order2][0] );
                                                                        npVals[index].imag ( self.eMatrices[bandIter][order1][order2][1] );
                                                                    }
                                                                }
                                                            }

                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleEMs ( npVals, []( void *f ) { std::complex<proshade_double>* foo = reinterpret_cast< std::complex<proshade_double>* > ( f ); delete foo; } );

                                                            //== Create the output object
                                                            pybind11::array_t < std::complex<proshade_double> > retArr = pybind11::array_t < std::complex<proshade_double > > (
                                                                            { self.maxShellBand, ( ( self.maxShellBand * 2 ) + 1 ), ( ( self.maxShellBand * 2 ) + 1 ) },
                                                                            { sizeof ( std::complex < proshade_double > ) * static_cast<int> ( ( ( self.maxShellBand * 2 ) + 1 ) * ( ( self.maxShellBand * 2 ) + 1 ) ),
                                                                              sizeof ( std::complex < proshade_double > ) * static_cast<int>   ( ( self.maxShellBand * 2 ) + 1 ),
                                                                              sizeof ( std::complex < proshade_double > ) },
                                                                            npVals,
                                                                            pyCapsuleEMs );
            
                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns the E matrix values (these are the integral over all spheres of ( c1^(l,m) * c2^(l,m') ) values) obtained when rotation function or self-rotation function are computed. The returned array has three dimensions, first being the band, second being the order1 and third being the order2. Please note that as negative indexing does not simply work, the order indexing starts from 0 - i.e. array[1][0][0] means band 1 ; order1 = -1 and order2 = -1." )
        .def                                          ( "getSO3Coefficients",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self ) -> pybind11::array_t < std::complex < proshade_double > >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            std::complex<proshade_double>* npVals = new std::complex < proshade_double >[static_cast<proshade_unsign> ( self.maxShellBand * ( ( self.maxShellBand * 2 ) + 1 ) * ( ( self.maxShellBand * 2 ) + 1 ) )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
    
                                                            //== Allocate local variables
                                                            proshade_signed index = 0;
                                                                                                                                                                
                                                            //== Fill with zeroes as the matrix will be sparse
                                                            for ( proshade_unsign iter = 0; iter < static_cast < proshade_unsign > ( self.maxShellBand * ( ( self.maxShellBand * 2 ) + 1 ) * ( ( self.maxShellBand * 2 ) + 1 ) ); iter++ ) { npVals[iter].real ( 0.0 );  npVals[iter].imag ( 0.0 ); }
    
                                                            //== Copy data to new memory
                                                            for ( proshade_signed bandIter = 0; bandIter < static_cast< proshade_signed > ( self.maxShellBand ); bandIter++ )
                                                            {
                                                                for ( proshade_unsign order1 = 0; order1 < ( ( bandIter * 2 ) + 1 ); order1++ )
                                                                {
                                                                    for ( proshade_unsign order2 = 0; order2 < ( ( bandIter * 2 ) + 1 ); order2++ )
                                                                    {
                                                                        index = order2 + ( ( self.maxShellBand * 2 ) + 1 ) * ( order1 + ( ( self.maxShellBand * 2 ) + 1 ) * bandIter );
                                                                        npVals[index].real ( self.so3Coeffs[self.so3CoeffsArrayIndex ( order1 - bandIter, order2 - bandIter, bandIter )][0] );
                                                                        npVals[index].imag ( self.so3Coeffs[self.so3CoeffsArrayIndex ( order1 - bandIter, order2 - bandIter, bandIter )][1] );
                                                                    }
                                                                }
                                                            }

                                                        //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                        pybind11::capsule pyCapsuleSOCoeffs ( npVals, []( void *f ) { std::complex<proshade_double>* foo = reinterpret_cast< std::complex<proshade_double>* > ( f ); delete foo; } );

                                                        //== Create the output object
                                                        pybind11::array_t < std::complex<proshade_double> > retArr = pybind11::array_t < std::complex<proshade_double > > (
                                                                        { self.maxShellBand, ( ( self.maxShellBand * 2 ) + 1 ), ( ( self.maxShellBand * 2 ) + 1 ) },
                                                                        { sizeof ( std::complex < proshade_double > ) * static_cast<int> ( ( ( self.maxShellBand * 2 ) + 1 ) * ( ( self.maxShellBand * 2 ) + 1 ) ),
                                                                          sizeof ( std::complex < proshade_double > ) * static_cast<int>   ( ( self.maxShellBand * 2 ) + 1 ),
                                                                          sizeof ( std::complex < proshade_double > ) },
                                                                        npVals,
                                                                        pyCapsuleSOCoeffs );
        
                                                        //== Done
                                                        return ( retArr );
                                                    }, "This function returns the SO(3) coefficient values (these are normalised E matrix values with sign modification) obtained when rotation function or self-rotation function are computed. The returned array has three dimensions, first being the band, second being the order1 and third being the order2. Please note that as negative indexing does not simply work, the order indexing starts from 0 - i.e. array[1][0][0] means band 1 ; order1 = -1 and order2 = -1." )
        .def                                          ( "getRotationFunctionMap",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self ) -> pybind11::array_t < std::complex < proshade_double > >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            std::complex<proshade_double>* npVals = new std::complex < proshade_double >[static_cast<proshade_unsign> ( ( self.maxShellBand * 2 ) * ( self.maxShellBand * 2 ) * ( self.maxShellBand * 2 ) )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
            
                                                            //== Copy the values
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( ( self.maxShellBand * 2 ) * ( self.maxShellBand * 2 ) * ( self.maxShellBand * 2 ) ); iter++ ) { npVals[iter].real ( self.so3CoeffsInverse[iter][0] ); npVals[iter].imag ( self.so3CoeffsInverse[iter][1] ); }
        
                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleRotMap ( npVals, []( void *f ) { std::complex<proshade_double>* foo = reinterpret_cast< std::complex<proshade_double>* > ( f ); delete foo; } );
                                                       
                                                            //== Create python readable object with the correct memory access
                                                            pybind11::array_t < std::complex < proshade_double > > retArr = pybind11::array_t < std::complex < proshade_double > > (
                                                                { ( self.maxShellBand * 2 ), ( self.maxShellBand * 2 ), ( self.maxShellBand * 2 ) },  // Shape
                                                                { ( self.maxShellBand * 2 ) * ( self.maxShellBand * 2 ) * sizeof(std::complex < proshade_double >),
                                                                  ( self.maxShellBand * 2 ) * sizeof(std::complex < proshade_double >),
                                                                  sizeof(std::complex < proshade_double >) },                                         // C-stype strides
                                                                npVals,                                                                               // Data
                                                                pyCapsuleRotMap );                                                                    // Capsule (destructor)

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns the (self) rotation function as a three-dimensional map of complex numbers." )
        .def                                          ( "getRotationMatrixFromSOFTCoordinates",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self, proshade_signed xPos, proshade_signed yPos, proshade_signed zPos ) -> pybind11::array_t < proshade_double >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            proshade_double* npVals = new proshade_double[9];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
        
                                                            //== Initialise local variables
                                                            proshade_double eulA, eulB, eulG;
            
                                                            //== Compute the Euler angles from SOFT position
                                                            ProSHADE_internal_maths::getEulerZXZFromSOFTPosition ( self.maxShellBand, xPos, yPos, zPos, &eulA, &eulB, &eulG );
            
                                                            //== Compute the rotation matrix
                                                            ProSHADE_internal_maths::getRotationMatrixFromEulerZXZAngles ( eulA, eulB, eulG, npVals );
    
                                                            //== Create capsule to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleRMSoft ( npVals, []( void *f ) { proshade_double* foo = reinterpret_cast< proshade_double* > ( f ); delete foo; } );
                                                   
                                                            //== Create python readable object with the correct memory access
                                                            pybind11::array_t < proshade_double > retArr = pybind11::array_t < proshade_double > ( { 3, 3 },
                                                                                                                                                   { 3 * sizeof(proshade_double), sizeof(proshade_double) },
                                                                                                                                                   npVals,
                                                                                                                                                   pyCapsuleRMSoft );

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function converts a given rotation function map position onto the corresponding rotation matrix.", pybind11::arg ( "xPos" ), pybind11::arg ( "yPos" ), pybind11::arg ( "zPos" ) )
        .def                                          ( "getTranslationFunctionMap",
                                                        [] ( ProSHADE_internal_data::ProSHADE_data &self ) -> pybind11::array_t < std::complex < proshade_double > >
                                                        {
                                                            //== Allocate memory for the numpy values
                                                            std::complex<proshade_double>* npVals = new std::complex < proshade_double >[static_cast<proshade_unsign> ( self.getXDim() * self.getYDim() * self.getZDim() )];
                                                            ProSHADE_internal_misc::checkMemoryAllocation ( npVals, __FILE__, __LINE__, __func__ );
        
                                                            //== Copy the values
                                                            for ( proshade_unsign iter = 0; iter < static_cast<proshade_unsign> ( self.getXDim() * self.getYDim() * self.getZDim() ); iter++ ) { npVals[iter].real ( self.translationMap[iter][0] ); npVals[iter].imag ( self.translationMap[iter][1] ); }
    
                                                            //== Create capsules to make sure memory is released properly from the allocating language (C++ in this case)
                                                            pybind11::capsule pyCapsuleTrsMap ( npVals, []( void *f ) { std::complex<proshade_double>* foo = reinterpret_cast< std::complex<proshade_double>* > ( f ); delete foo; } );
                                                   
                                                            //== Create python readable object with the correct memory access
                                                            pybind11::array_t < std::complex < proshade_double > > retArr = pybind11::array_t < std::complex < proshade_double > > (
                                                                { self.getXDim(), self.getYDim(), self.getZDim() },  // Shape
                                                                { self.getYDim() * self.getZDim() * sizeof(std::complex < proshade_double >),
                                                                  self.getZDim() * sizeof(std::complex < proshade_double >),
                                                                  sizeof(std::complex < proshade_double >) },                                         // C-stype strides
                                                                npVals,                                                                               // Data
                                                                pyCapsuleTrsMap );                                                                    // Capsule (destructor)

                                                            //== Done
                                                            return ( retArr );
                                                        }, "This function returns the translation function as a three-dimensional map of complex numbers." )
    
        //============================================ Member variables
        .def_readwrite                                ( "fileName",          &ProSHADE_internal_data::ProSHADE_data::fileName      )
        .def_readwrite                                ( "xDimSize",          &ProSHADE_internal_data::ProSHADE_data::xDimSize      )
        .def_readwrite                                ( "yDimSize",          &ProSHADE_internal_data::ProSHADE_data::yDimSize      )
        .def_readwrite                                ( "zDimSize",          &ProSHADE_internal_data::ProSHADE_data::zDimSize      )
        .def_readwrite                                ( "aAngle",            &ProSHADE_internal_data::ProSHADE_data::aAngle        )
        .def_readwrite                                ( "bAngle",            &ProSHADE_internal_data::ProSHADE_data::bAngle        )
        .def_readwrite                                ( "cAngle",            &ProSHADE_internal_data::ProSHADE_data::cAngle        )
        .def_readwrite                                ( "xDimIndices",       &ProSHADE_internal_data::ProSHADE_data::xDimIndices   )
        .def_readwrite                                ( "yDimIndices",       &ProSHADE_internal_data::ProSHADE_data::yDimIndices   )
        .def_readwrite                                ( "zDimIndices",       &ProSHADE_internal_data::ProSHADE_data::zDimIndices   )
        .def_readwrite                                ( "xGridIndices",      &ProSHADE_internal_data::ProSHADE_data::xGridIndices  )
        .def_readwrite                                ( "yGridIndices",      &ProSHADE_internal_data::ProSHADE_data::yGridIndices  )
        .def_readwrite                                ( "zGridIndices",      &ProSHADE_internal_data::ProSHADE_data::zGridIndices  )
        .def_readwrite                                ( "xAxisOrder",        &ProSHADE_internal_data::ProSHADE_data::xAxisOrder    )
        .def_readwrite                                ( "yAxisOrder",        &ProSHADE_internal_data::ProSHADE_data::yAxisOrder    )
        .def_readwrite                                ( "zAxisOrder",        &ProSHADE_internal_data::ProSHADE_data::zAxisOrder    )
        .def_readwrite                                ( "xAxisOrigin",       &ProSHADE_internal_data::ProSHADE_data::xAxisOrigin   )
        .def_readwrite                                ( "yAxisOrigin",       &ProSHADE_internal_data::ProSHADE_data::yAxisOrigin   )
        .def_readwrite                                ( "zAxisOrigin",       &ProSHADE_internal_data::ProSHADE_data::zAxisOrigin   )
        .def_readwrite                                ( "xCom",              &ProSHADE_internal_data::ProSHADE_data::xCom          )
        .def_readwrite                                ( "yCom",              &ProSHADE_internal_data::ProSHADE_data::yCom          )
        .def_readwrite                                ( "zCom",              &ProSHADE_internal_data::ProSHADE_data::zCom          )
        .def_readwrite                                ( "xFrom",             &ProSHADE_internal_data::ProSHADE_data::xFrom         )
        .def_readwrite                                ( "yFrom",             &ProSHADE_internal_data::ProSHADE_data::yFrom         )
        .def_readwrite                                ( "zFrom",             &ProSHADE_internal_data::ProSHADE_data::zFrom         )
        .def_readwrite                                ( "xTo",               &ProSHADE_internal_data::ProSHADE_data::xTo           )
        .def_readwrite                                ( "yTo",               &ProSHADE_internal_data::ProSHADE_data::yTo           )
        .def_readwrite                                ( "zTo",               &ProSHADE_internal_data::ProSHADE_data::zTo           )
        .def_readwrite                                ( "spherePos",         &ProSHADE_internal_data::ProSHADE_data::spherePos     )
        .def_readwrite                                ( "noSpheres",         &ProSHADE_internal_data::ProSHADE_data::noSpheres     )
        .def_readwrite                                ( "maxShellBand",      &ProSHADE_internal_data::ProSHADE_data::maxShellBand  )
        .def_readwrite                                ( "isEmpty",           &ProSHADE_internal_data::ProSHADE_data::isEmpty       )
        .def_readwrite                                ( "inputOrder",        &ProSHADE_internal_data::ProSHADE_data::inputOrder    )
        
        //============================================ Description
        .def                                          ( "__repr__", [] ( const ProSHADE_internal_data::ProSHADE_data &a ) { return "<ProSHADE_data class object> (This class contains all information, results and available functionalities for a structure)"; } );
}
