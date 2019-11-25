AddStoragePolicy = {
  "storagePolicyName": "cs-15",
  "copyName": "Primary",
  "useGlobalPolicy": {
      "storagePolicyName": "GDP_INFRA_DC1"
  },
    "storagePolicyFlags": {
        "blockLevelDedup": 1,
        "enableGlobalDeduplication": 1
    },
  "storagePolicyCopyInfo": {
      "active": 1,
      "isDefault": 1,
      "hardWareCompression": 1,
      "spareMediaGroup": {
          "spareMediaGroupName": ""
      },
      "dedupeFlags": {
          "enableDASHFull": 1,
          "pauseAndRecoverCurrentDDB": 1,
          "useGlobalDedupStore": 1,
          "hostGlobalDedupStore": 1,
          "automaticallyPauseAndRecoverDDB": 1,
          "enableDeduplication": 1,
          "enableClientSideDedup": 1
      },
      "retentionRules": {
          "retainBackupDataForCycles": -1,
          "retainArchiverDataForDays": -1,
          "retainBackupDataForDays": -1,
          "retentionFlags": {

          }
      },
      "DDBPartitionInfo": {
          "maInfoList": [{
              "mediaAgent": {
                  "mediaAgentName": "win-826lfdml7cl_FOI"
              },
              "subStoreList": [{
                  "accessPath": {
                      "path": "d:\\1"
                  }
              }]
          }]
      },
      "drivePool": {
          "drivePoolName": ""
      },
      "copyFlags": {
          "autoAddDataPaths": 2
      },
      "library": {
          "libraryName": "DISKLIB_INFRA"
      },
      "mediaAgent": {
          "mediaAgentName": "win-826lfdml7cl_FOI"
      }
  },
  "incrementalStoragePolicy": {
      "storagePolicyName": "GDP_INFRA_DC1"
  }
}