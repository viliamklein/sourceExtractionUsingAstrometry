#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <utility>

#include <coz.h>

extern "C" {
#include <astrometry/log.h>
#include <astrometry/errors.h>
#include <astrometry/simplexy.h>
#include <astrometry/image2xy.h>
#include <fitsio.h>
}

int main(int argc, char *argv[])
{
    // Parse args
    float dpsf = atof(argv[1]);

    simplexy_t xyparams;
    simplexy_fill_in_defaults(&xyparams);
    simplexy_set_defaults(&xyparams);
    xyparams.nobgsub = false; // turn off/on background sub
    xyparams.dpsf = dpsf;
    xyparams.dlim = 30;

    int status = 0;
    fitsfile *fptr;

    int naxis, bitpix;
    long naxisn[3];
    int nhdus, hdutype;

    fits_open_file(&fptr, argv[2], READONLY, &status);
    if(status) fits_report_error(stderr, status);
    fits_get_num_hdus(fptr, &nhdus, &status);

    fits_movabs_hdu(fptr, 1, &hdutype, &status);
    fits_get_hdu_type(fptr, &hdutype, &status);
    fits_get_img_dim(fptr, &naxis, &status);
    fits_get_img_size(fptr, 2, naxisn, &status);
    fits_get_img_type(fptr, &bitpix, &status);

    std::vector<float> image(naxisn[0] * naxisn[1]);
    xyparams.image = &image[0];
    std::vector<long> fpixel(naxis, 1);
    fits_read_pix(fptr, TSHORT, &fpixel[0], naxisn[0]*naxisn[1], NULL, xyparams.image, NULL, &status);
    // COZ_PROGRESS;

    xyparams.nx = naxisn[0];
    xyparams.ny = naxisn[1];

    // for(int ii=0; ii<10; ii++){
        // simplexy_run(&xyparams);
        // COZ_BEGIN("SOURCE-EXTRACT");
    image2xy_run(&xyparams, 2, false);
        // COZ_END("SOURCE-EXTRACT");

    //     xyparams.image = &image[0];
    //     fits_read_pix(fptr, TFLOAT, &fpixel[0], naxisn[0]*naxisn[1], NULL, xyparams.image, NULL, &status);
    // }

    std::vector<float> xx(xyparams.x, xyparams.x+xyparams.npeaks);
    std::vector<float> yy(xyparams.y, xyparams.y+xyparams.npeaks);
    // std::pair<std::vector<float>, std::vector<float>> pt(xx, yy);

    fits_close_file(fptr, &status);
    std::ofstream xyList;
    std::stringstream datLine;
    std::string line;

    // xyList.open("xyList.dat");
    // datLine << std::fixed;
    // datLine << std::setprecision(4);
    // for ( auto ix = xx.begin(), iy = yy.begin(); (ix != xx.end()) && (iy != yy.end()); ix++, iy++){
    //     datLine << *ix << ", " << *iy << "\n";
    //     xyList << datLine.str();
    //     datLine.str(std::string());
    // }
    // xyList.close();

    std::cout << "Found " << xx.size() << " sources\n";
    std::cout << std::fixed;
    std::cout << std::setprecision(4);
    for ( auto ix = xx.begin(), iy = yy.begin(); (ix != xx.end()) && (iy != yy.end()); ix++, iy++){
        std::cout << *ix << ", " << *iy << "\n";
    }


    return 0;
}