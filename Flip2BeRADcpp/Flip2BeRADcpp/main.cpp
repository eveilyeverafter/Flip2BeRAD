//
//  main.cpp
//  Flip2BeRADcpp
//
//  Created by Tyler Hether on 4/28/16.
//  Copyright © 2016 Tyler Hether. All rights reserved.
//

#include <iostream>
#include <string>
#include <fstream>
#include <limits>
#include <cstdlib>

//std::fstream& GotoLine(std::fstream& file, unsigned int num)
//{
//    file.seekg(std::ios::beg);
//    for(unsigned int i=0; i < num - 1; ++i)
//    {
//        file.ignore(std::numeric_limits<std::streamsize>::max(),'\n');
//    }
//    return file;
//}



int main(int argc, const char * argv[]) {
    using namespace std;
    
    /*
     *
     * Open output files
     *
     */
    
        // Inputs
        fstream forward_file;
        fstream reverse_file;
        fstream barcodes_file;
    
        // Outputs
        ofstream nobarcodes_forward;
        ofstream nobarcodes_reverse;
        ofstream barcode_no_cut_forward;
        ofstream barcode_no_cut_reverse;
        ofstream barcode_yes_cut_forward;
        ofstream barcode_yes_cut_reverse;

        nobarcodes_forward.open("barcode_no_cut_forward.fastq");
        nobarcodes_reverse.open("nobarcodes_reverse.fastq");
        barcode_no_cut_forward.open("barcode_no_cut_forward.fastq");
        barcode_no_cut_reverse.open("barcode_no_cut_reverse.fastq");
        barcode_yes_cut_forward.open("barcode_yes_cut_forward.fastq");
        barcode_yes_cut_reverse.open("barcode_yes_cut_reverse.fastq");

    /*
     *
     * Set Default parameter values
     *
     */

        int n_mismatch = 0;
        string cutsite = "TGCAT";
        int quiet = 0;
        string forward_file_name;
        string reverse_file_name;
        string barcodes_file_name;
    
    /*
     *
     * user override of defaults
     *
     */

        // Search for the quiet flag
        for(int i=1; i<argc; i++)
        {
            if(string(argv[i]) == "-q"){
                quiet = atoi(argv[i+1]);
                if(quiet == 0)
                {
                    cout << "Verbose printing is on. To run quietly, use the '-q 1' flag." << endl;
                }
            }
        }

        if (!quiet){
            cout << "Parameters: " << endl;
        }
    
        for(int i=1; i<argc; i++)
        {
            if(string(argv[i]) == "-m"){
                n_mismatch = atoi(argv[i+1]);
                if (!quiet)
                {
                    cout << "\tNumber of mismatches bases allowed in barcode sequence: " << n_mismatch << endl;
                }
            }
            if(string(argv[i]) == "-f")
            {
                forward_file_name = argv[i+1];
                if (!quiet)
                {
                    cout << "\tThe forward fastq file: " << forward_file_name << endl;
                }
                forward_file.open (forward_file_name);
            }
            if(string(argv[i]) == "-r")
            {
                reverse_file_name = argv[i+1];
                if (!quiet)
                {
                    cout << "\tThe reverse fastq file: " << reverse_file_name << endl;
                }
                reverse_file.open (reverse_file_name);
            }
            if(string(argv[i]) == "-b")
            {
                barcodes_file_name = argv[i+1];
                if (!quiet)
                {
                    cout << "\tThe barcodes file: " << barcodes_file_name << endl;
                }
                barcodes_file.open (barcodes_file_name);
            }
            if(string(argv[i]) == "-c")
            {
                string cutsite = argv[i+1];
                if (!quiet)
                {
                    cout << "\tThe cut site(s): " << cutsite << endl;
                }
            }
        }

    
     /*
      * Error checking to make sure the input files exists
      */
    
        cout << endl;
            if( ! forward_file ) {
                cout << "Error opening forward file" << endl ;
                return -1 ;
            }
        if( ! reverse_file ) {
            cout << "Error opening reverse file" << endl ;
            return -1 ;
        }
        if( ! barcodes_file ) {
            cout << "Error opening barcodes file" << endl ;
            return -1 ;
        }
    
    /* This block checks that the paired-end files are the same length. 
     * It's also needed to store the number of lines.
     */
    
        string line;
        int number_of_lines_forward = 0;
        int number_of_lines_reverse = 0;
    
        fstream forward_file1, reverse_file1;
    
        cout << "Checking to make sure forward and reverse files are the same length..." << endl;
        forward_file1.open (forward_file_name);
        reverse_file1.open (reverse_file_name);
        
        while (std::getline(forward_file1, line)){
            ++number_of_lines_forward;
        }
        cout << "The number of lines in the forward fastq is " << number_of_lines_forward << endl;
        
        while (std::getline(reverse_file1, line)){
            ++number_of_lines_reverse;
        }
        cout << "The number of lines in the reverse fastq is " << number_of_lines_reverse << endl;
        
        forward_file1.close();
        reverse_file1.close();
    
        if (number_of_lines_forward != number_of_lines_reverse)
        {
            cout << "Input fastq files need the same length. Aborting." << endl;
            return (1);
        }

    /*
     * Now begin the actual algorithm to flip reads, if necessary.
     */

    
    
    string f_line1, f_line2, f_line3, f_line4;
    string r_line1, r_line2, r_line3, r_line4;
    
    for(int i = 0; i < number_of_lines_forward; i++)
    {
        getline(forward_file, f_line1);
        getline(forward_file, f_line2);
        getline(forward_file, f_line3);
        getline(forward_file, f_line4);

        getline(reverse_file, r_line1);
        getline(reverse_file, r_line2);
        getline(reverse_file, r_line3);
        getline(reverse_file, r_line4);
        
        cout << "f line " << i << ": " << f_line1 << endl;
        cout << "f line " << i+1 << ": " << f_line2 << endl;
        cout << "f line " << i+2 << ": " << f_line3 << endl;
        cout << "f line " << i+3 << ": " << f_line4 << endl;
        
        cout << "r line " << i << ": " << r_line1 << endl;
        cout << "r line " << i+1 << ": " << r_line2 << endl;
        cout << "r line " << i+2 << ": " << r_line3 << endl;
        cout << "r line " << i+3 << ": " << r_line4 << endl;
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        i += 3;
    }
    
    
//    
//    while (getline(forward_file, f_line1) && !f_line1.empty())
//    {
//        getline(forward_file, f_line2);
//        getline(forward_file, f_line3);
//        getline(forward_file, f_line4);
//        number_of_lines_forward += 4;
//        
//    }
//    
//    cout << "The number of lines in the forward fastq is " << number_of_lines_forward << endl;
//    
//    
    
//    cout << forward_file_name << endl;
    
    
    
//    for (int i=0; i<1e6; i++){
//        nobarcodes_forward << i << endl;
//    }
//    
    
//    string content;
//    while(forward_file >> content) {
//        cout << content << ' ';
//    }
    
    
//    ifstream infile;
//    infile.open("../../examples/forward_test.fastq");
//    string sLine;
//    
//    while (!infile.eof())
//    {
//        infile >> sLine;
//        cout << sLine.data() << endl;
//        
//    }
//    infile.close();

    
//        string sLine;
//        while (!reverse_file.eof())
//        {
//            reverse_file >> sLine;
//            cout << sLine.data() << endl;
//    
//        }


    


    /*
     *
     * Close files
     *
     */
    forward_file.close();
    reverse_file.close();
    
    nobarcodes_forward.close();
    nobarcodes_reverse.close();
    barcode_no_cut_forward.close();
    barcode_no_cut_reverse.close();
    barcode_yes_cut_forward.close();
    barcode_yes_cut_reverse.close();

    
    
    return 0;
}
