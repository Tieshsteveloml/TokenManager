- installation
    # pip3 install -r requirements.txt
- configuration
    In the config.py
    * copy the input csv file to this directory
	* replace input csv file name to SOURCE_FILE_NAME
	* replace output csv file name to OUTPUT_FILE_NAME
    * replace destination address to DEST_ADDRESS
    * if you want test_net, change USING_TEST_NET to True
    * if you want test_net, change USING_TEST_NET to True, in test_net case, you must change contract address as well
    * you can change gas price as GAS_PRICE
	* you can change gas limit as GAS_LIMIT
    * SLEEP_TIME_PER_ADDRESS: wait time per addresses
- run
    # python3 main.py