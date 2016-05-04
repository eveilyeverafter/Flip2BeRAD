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
#include <vector>


//std::fstream& GotoLine(std::fstream& file, unsigned int num)
//{
//    file.seekg(std::ios::beg);
//    for(unsigned int i=0; i < num - 1; ++i)
//    {
//        file.ignore(std::numeric_limits<std::streamsize>::max(),'\n');
//    }
//    return file;
//}
using namespace std;

// Forward Declarations of Functions:


bool in_array(string query, string *test_array, int length_of_array)
{
//    vector<string> query{barcodes[0]};
//    vector<string> test{barcodes[0]};
    for(int i=0; i < length_of_array; i++)
    {
        if(query == test_array[i])
        {
            return true;
        }
    }
    
    return false;
    
}


bool adjacent_cutsite(string query, string given_cutsites)
{
    if (given_cutsites.find(query) == 0)
    {
        std::cout << "The cutsite is next to the barcode:\n";
        return true;
    } else
    {
        return false;
    }
}


int main(int argc, const char * argv[]) {

    std::ios_base::sync_with_stdio(false);
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

    nobarcodes_forward.open("nobarcodes_forward.fastq");
    nobarcodes_reverse.open("nobarcodes_reverse.fastq");
    barcode_no_cut_forward.open("barcode_no_cut_forward.fastq");
    barcode_no_cut_reverse.open("barcode_no_cut_reverse.fastq");
    barcode_yes_cut_forward.open("filtered_forward.fastq");
    barcode_yes_cut_reverse.open("filtered_reverse.fastq");

/*
 *
 * Set Default parameter values
 *
 */

    int n_mismatch = 0; // Right now this is not set.
    string cutsite = "TGCAT";
    int quiet = 0;
    string forward_file_name;
    string reverse_file_name;
    string barcodes_file_name;
    int offset = 0;
    int n_bp_search = 20; // This parameter specifies the number of bps to search pass a barcode for a cut site.
    
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
        if(string(argv[i]) == "-o"){
            offset = atoi(argv[i+1]);
            if (!quiet && offset > 0)
            {
                cout << "\tBarcode searching will be offset by " << offset << " basepairs." << endl;
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
 *
 * Error checking to make sure the input files exists
 *
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
    
/*
 *
 * Pull the barcodes into memory.
 *
 */
    
    cout << "Reading barcodes file." << endl;
    int number_of_lines_barcodes(0);
    fstream barcodes_file1;
    barcodes_file1.open (barcodes_file_name);
    string line;
    while (getline(barcodes_file1, line)){
        ++number_of_lines_barcodes;
    }
    barcodes_file1.close();
    cout << "The number of barcodes provided: " << number_of_lines_barcodes << "." << endl;
    
    string *barcodes = new string[number_of_lines_barcodes];
    
    for(int i=0; i < number_of_lines_barcodes; i++)
    {
        getline(barcodes_file, line);
        barcodes[i] = line;
    }

    // Check to make sure all barcodes are the same length.
    int barcode_length = static_cast<int>(barcodes[0].length());
    
    cout << "Barcode length: " << barcode_length << "." << endl;
    for(int i=1; i < number_of_lines_barcodes; i++)
    {
        if(barcode_length != barcodes[i].length())
        {
            cout << "\nError: All barcodes need to be the same length." << endl;
            cout << "The first barcode was " << barcode_length << " bps but barcode #" << i+1 << " was " << barcodes[i].length() << " bps long. Aborting." << endl;
            return (2);
        }
    }
    cout << "Do all barcodes have the same length?... Check." << endl;
    
    // Testing.
//        for(int i=0; i < number_of_lines_barcodes; i++)  cout << barcodes[i] << endl;
    
    
    
/*
 * This block checks that the paired-end files are the same length.
 * It's also needed to store the number of lines.
 * This block is really slow...
 */
    
//    int number_of_lines_forward = 10000;
//    int number_of_lines_reverse = 0;
//
//    fstream forward_file1, reverse_file1;
//
//    cout << "Checking to make sure forward and reverse files are the same length..." << endl;
//    forward_file1.open (forward_file_name);
//    reverse_file1.open (reverse_file_name);
//        
//    while (std::getline(forward_file1, line)){
//        ++number_of_lines_forward;
//    }
//    cout << "The number of lines in the forward fastq is " << number_of_lines_forward << endl;
//        
//    while (std::getline(reverse_file1, line)){
//        ++number_of_lines_reverse;
//    }
//    cout << "The number of lines in the reverse fastq is " << number_of_lines_reverse << endl;
//        
//    forward_file1.close();
//    reverse_file1.close();
//    
//    if (number_of_lines_forward != number_of_lines_reverse)
//    {
//        cout << "Input fastq files need the same length. Aborting." << endl;
//        return (1);
//    }

/*
 *
 * Now begin the actual algorithm to flip reads, if necessary.
 *
 */
    
    // For storing various reads counts:
    int n_barcodes_found = 0;
    int n_barcodes_on_forward = 0;
    int n_barcodes_on_reverse = 0;
    int n_reads_with_no_barcode = 0;
    int n_reads_with_barcode_no_cut = 0;
    int n_reads_with_barcode_yes_cut = 0;
    
    
    string f_line1, f_line2, f_line3, f_line4;
    string r_line1, r_line2, r_line3, r_line4;
    long long unsigned int count(0); // Testing...
//    for(int i = 0; i < number_of_lines_forward; i++)
//    {
    while( !forward_file.eof() )
    {
        count +=1;
        if(count % 10000 == 0){
            cout << "Processing read " << count << "..." << endl;
        }
        // Get the fastq info for the forward and reverse read...
        getline(forward_file, f_line1);
        getline(forward_file, f_line2);
        getline(forward_file, f_line3);
        getline(forward_file, f_line4);

        getline(reverse_file, r_line1);
        getline(reverse_file, r_line2);
        getline(reverse_file, r_line3);
        getline(reverse_file, r_line4);

// Testing...
//        cout << "f line " << i << ": " << f_line1 << endl;
//        cout << "f line " << i+1 << ": " << f_line2 << endl;
//        cout << "f line " << i+2 << ": " << f_line3 << endl;
//        cout << "f line " << i+3 << ": " << f_line4 << endl;
//        
//        cout << "r line " << i << ": " << r_line1 << endl;
//        cout << "r line " << i+1 << ": " << r_line2 << endl;
//        cout << "r line " << i+2 << ": " << r_line3 << endl;
//        cout << "r line " << i+3 << ": " << r_line4 << endl;
        
        /* Determine if there's a barcode on either the forward or reverse read.
         * If there isn't, output the read to the nobarcodes_forward and nobarcodes_reverse
         * files.
         *
         */
        
        string f_query = f_line2.substr(offset,barcode_length);
        string r_query = r_line2.substr(offset,barcode_length);
        
        if(in_array(f_query, barcodes, number_of_lines_barcodes) | in_array(r_query, barcodes, number_of_lines_barcodes))
        {
            n_barcodes_found += 1;
        
            /* Is there a cut site next to the barcode on either read? If
             * not, output to a 'remainder file'. If on the forward, print to
             * main filtered files. If on reverse, print the flipped pair to file.
             */
            if (in_array(f_query, barcodes, number_of_lines_barcodes))
            {
                n_barcodes_on_forward += 1;
                
                string f_query2 = f_line2.substr(offset+barcode_length, n_bp_search);
                if(f_query2.find(cutsite) == 0)
                {
                    n_reads_with_barcode_yes_cut += 1;
                    //cout << cutsite << " is in " << f_query2 << endl;
                    barcode_yes_cut_forward << f_line1 << "\n" << f_line2 << "\n" << f_line3 << "\n" << f_line4 << "\n";
                    barcode_yes_cut_reverse << r_line1 << "\n" << r_line2 << "\n" << r_line3 << "\n" << r_line4 << "\n";
                    
                } else
                {
                    n_reads_with_barcode_no_cut += 1;
                    barcode_no_cut_forward << f_line1 << "\n" << f_line2 << "\n" << f_line3 << "\n" << f_line4 << "\n";
                    barcode_no_cut_reverse << r_line1 << "\n" << r_line2 << "\n" << r_line3 << "\n" << r_line4 << "\n";
                }
                
            } else
            {
                // barcode is on the reverse if not on the forward in this block...
                n_barcodes_on_reverse += 1;
                
                string r_query2 = r_line2.substr(offset+barcode_length, n_bp_search);
                if(r_query2.find(cutsite) == 0)
                {
                    n_reads_with_barcode_yes_cut += 1;
                    barcode_yes_cut_reverse << f_line1 << "\n" << f_line2 << "\n" << f_line3 << "\n" << f_line4 << "\n";
                    barcode_yes_cut_forward << r_line1 << "\n" << r_line2 << "\n" << r_line3 << "\n" << r_line4 << "\n";
                } else
                {
                    n_reads_with_barcode_no_cut += 1;
                    barcode_no_cut_forward << f_line1 << "\n" << f_line2 << "\n" << f_line3 << "\n" << f_line4 << "\n";
                    barcode_no_cut_reverse << r_line1 << "\n" << r_line2 << "\n" << r_line3 << "\n" << r_line4 << "\n";
                }
            }
        } else
        {
            n_reads_with_no_barcode += 1;
            nobarcodes_forward << f_line1 << "\n" << f_line2 << "\n" << f_line3 << "\n" << f_line4 << "\n";
            nobarcodes_reverse << r_line1 << "\n" << r_line2 << "\n" << r_line3 << "\n" << r_line4 << "\n";
            
        }
        
       
        
        
        
        // This block is for Testing...
        //        if(in_array(f_query, barcodes, number_of_lines_barcodes))
        //        {
        //            count += 1;
        //            cout << "alright " << count << endl;
        //        }
        //        else
        //        {
        //            cout << "oh no!" << endl;
        //        }
        
        
        
//        cout << "Here you go: " << f_query << endl;
//
//        cout << "The size of a barcode is " << barcodes[0].length() << " bytes." << endl;
//        
        
        
//        i += 3;
    }
//    
//    string str="CACTTCGA";
//    string str2 = str.substr (3,5);
////    string str3 = str.substr (3,5);
////    cout << str2 << endl;
////    if (str2 == str3) cout << "yes" << endl;
////    
//    // To do. determine how to find if a substr is in an array of strings.
//
////    std::string myinput;
//    std::vector<std::string> mylist{str};
//    
//    if (std::find(std::begin(mylist), std::end(mylist), str2) == std::end(mylist))
//    {
//        cout << str2 << " is in the list."<< endl;
//    }
    
//    std::cin >> myinput;
    
//    string query;

    
    

    
    
    
/*
 *
 * Summary output.
 *
 */
    
    cout << "\nSummary:\nNumber of reads without barcodes: " << n_reads_with_no_barcode << " (out of " << count-1 << " pairs)" << endl;
    cout << "Number of reads found with barcodes: " << n_barcodes_found << " (out of " << count-1 << " pairs)" << endl;
    

    cout << "Of the " << n_barcodes_found << " reads containing barcodes, " << n_barcodes_on_forward << " were found on\nthe forward and " << n_barcodes_on_reverse << " were found on the paired-end read." << endl;
    
    cout << "Of the " << n_barcodes_found << " reads containing barcodes, " << n_reads_with_barcode_yes_cut << " had adjacent cut sites (" << n_reads_with_barcode_no_cut-1 << " did not)." << endl;

    
    //Testing block.
    std::string s("TGCAGABCDEFGHIJ");
    
    if (s.find(cutsite) == 0)
    {
        std::cout << "String starts with Hello\n";
    }
    
    
    
    
    
    
    
    
    
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

/*
 *
 * Free memory.
 *
 */
    
    delete[] barcodes;
    
/*
 *
 * Exit.
 *
 */
    
    return 0;

}


