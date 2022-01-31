//////////////////////////// Information on CGI Web-Server Program – Created by Rahul (22/11/2020) ////////////////////////////////

Implementation Approach – The program was created by methodological approach by retrieving configuration and related error handling
                        Establish Connection with client
                        Generate/extract all required information in sections (file-type, headers-list, variables etc) from client data
                        Set all basic environment variables (Server and client ports, addresses, headers etc)
                        Fork process; determine request type in child and execute task accordingly.

Code structure –  Follows functional-programming principles where code encapsulation is 
                    practiced and redundant code is replaced by general getter methods. All sections of 
                    code are organised by their role and implementation.

Code style – Style is similar to PEP-8 with minor personal preferences such as separation 
            of code within complex conditional branches with space for easy readability, using brackets 
            within if-else statements when complex logic present, space after every function, naming using Snake-Case 

Code Commenting –  The commenting was implemented such that each function is described by 
                    its Role (general operation) followed by brief description where necessary. Comments in 
                    between sections of code are included when complex conditional logic present or special 
                    cases are being considered, such as Extension- gzip compressed file

Testing –  config, cgibin and static files folders have been included for testing, these are required for tests to work!
Please DON’T remove.

P.S. To test Extension run - tests/gzip_test.sh
Assumptions - I was not able to achieve clarity from Ed on what type of files gzip should handle so I covered all those that were in static folder (html,txt,js,etc)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////