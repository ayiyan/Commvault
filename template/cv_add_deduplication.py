AddDeduplicationPolicy = {
  "storagePolicyName": "GDP_INFRA_DC1",
  "type": 1,
  "copyName": "GDP_INFRA_DC1_Primary",
  "numberOfCopies": 1,
  "clientGroup": {
    "_type_": 28,
    "clientGroupId": 0,
    "clientGroupName": ""
  },
  "storagePolicyCopyInfo": {
    "copyType": 1,
    "isFromGui": True,
    "active": 1,
    "isDefault": 1,
    "numberOfStreamsToCombine": 1,
    "dedupeFlags": {
      "enableDASHFull": 1,
      "hostGlobalDedupStore": 1,
      "enableDeduplication": 1
    },
    "storagePolicyFlags": {
      "blockLevelDedup": 1,
      "enableGlobalDeduplication": 1
    },
    "DDBPartitionInfo": {
      "maInfoList": [
        {
          "mediaAgent": {
            "mediaAgentId": 3,
            "_type_": 11,
            "mediaAgentName": "win-826lfdml7cl_FOI"
          },
          "subStoreList": [
            {
              "diskFreeWarningThreshholdMB": 10240,
              "diskFreeThresholdMB": 5120,
              "accessPath": {
                "path": "D:\\DDBB_INFRA"
              }
            }
          ]
        }
      ]
    },
    "library": {
      "libraryName": "DISKLIB_INFRA",
      "_type_": 0,
      "libraryId": 0
    },
    "mediaAgent": {
      "mediaAgentId": 3,
      "_type_": 11,
      "mediaAgentName": "win-826lfdml7cl_FOI"
    }
  }
}