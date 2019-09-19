# tfs_audit
Release audit for TFS Server

Python Version Used : 3.7.2

This was created to fulfill an audit requirement where the auditors wanted a list of all releases to our production environments between certain dates with the date, name, environment and comments. We put our change request details into the comments on each release so the change request number is also extracted.

The config file contains the environment information (you could replace this with argparse).

The only thing of interest in this is the use of the continuation token on the TFS server. By default TFS only provides 50 results and puts a continuation token in the header response. So this will check if it is present and if so make another request for the next data set until the token is no longer present. 
This was very hard to understand looking at the TFS API documentation as it didn't explain how to get the continuation token, thanks to Ference Bodie who asked microsoft, then figured it out themself and posted what they learnt.
