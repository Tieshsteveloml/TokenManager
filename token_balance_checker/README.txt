- installation
    # pip3 install -r requirements.txt
- configuration
    In the config.py
    * copy the input csv file to this directory
    * replace input csv file name to SOURCE_FILE_NAME
	* replace output csv file name to OUTPUT_FILE_NAME
    * if you want test_net, change USING_TEST_NET to True, in test_net case, you must change contract address as well
    * SLEEP_TIME_PER_ADDRESS: wait time per addresses
- run
    # python3 main.py