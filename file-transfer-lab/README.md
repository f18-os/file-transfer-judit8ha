# FILE-TRANSFER

*   `ClientServer.py` 
    * Supports "put" function and sends files to server
 .
    * Supports `./END` command.  It allows for graceful exit once 
     client disconnects. 
    *  handles messages and files differently. 

*  `fServer` 
    * Handles files and messages differently.  
    * Understands when a client disconnects it displays message and gracefully exits. 
    * Supports multiple clients with `fork()`
    * Displays message if file already exists. 
    * displays zero length messages and files. 
