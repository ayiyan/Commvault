SchedPolicy_BRONZE =  {
  "processinginstructioninfo": {},
  "taskInfo": {
    "task": {
      "taskType": 4,
      "policyType": 0,
      "taskName": "Sched_Share_BRONZE",
      "description" : "Bronze Sched Policy"
    },
    "appGroup": {
      "appTypes": [
        {
          "appTypeName": "Virtual Server"
        }
      ]
    },
    "subTasks": [
      {
        "subTaskOperation": 1,
        "subTask": {
          "subTaskName": "Synthetic_FULL",
          "subTaskType": 2,
          "operationType": 2,
          "subTaskId": 1
        },
        "pattern": {
          "active_end_occurence": 0,
          "freq_subday_interval": 0,
          "freq_type": 8,
          "description": "",
          "active_end_time": 0,
          "active_start_time": 10800,
          "active_start_date": 0,
          "freq_interval": 2,
          "freq_recurrence_factor": 1,
          "timeZone": {
            "TimeZoneName": ""
          }
        },
        "options": {
          "backupOpts": {
            "truncateLogsOnSource": False,
            "sybaseSkipFullafterLogBkp": False,
            "notSynthesizeFullFromPrevBackup": False,
            "backupLevel": 4,
            "incLevel": 1,
            "adHocBackup": False,
            "runIncrementalBackup": False,
            "doNotTruncateLog": False,
            "vsaBackupOptions": {
              "backupFailedVMsOnly": False
            },
            "cdrOptions": {
              "incremental": False,
              "dataVerificationOnly": False,
              "full": False
            },
            "dataOpt": {
              "skipCatalogPhaseForSnapBackup": True,
              "useCatalogServer": True,
              "followMountPoints": True,
              "enforceTransactionLogUsage": False,
              "skipConsistencyCheck": False,
              "createNewIndex": False,
              "autoCopy": False
            },
            "distAppsBackupOptions": {
              "runLogBkp": False,
              "runDataBkp": False
            },
            "mediaOpt": {}
          },
          "adminOpts": {
            "contentIndexingOption": {
              "subClientBasedAnalytics": False
            }
          },
          "commonOpts": {
            "perfJobOpts": {}
          }
        }
      },
      {
        "subTaskOperation": 1,
        "subTask": {
          "subTaskName": "Incremental",
          "subTaskType": 2,
          "operationType": 2,
          "subTaskId": 1
        },
        "pattern": {
          "active_end_occurence": 0,
          "freq_subday_interval": 0,
          "freq_type": 8,
          "description": "Every day at 21:00  starting 17 January, 2018 ",
          "active_end_time": 0,
          "active_start_time": 10800,
          "active_start_date": 0,
          "freq_interval": 125,
          "freq_recurrence_factor": 1,
          "timeZone": {
            "TimeZoneName": ""
          }
        },
        "options": {
          "backupOpts": {
            "truncateLogsOnSource": False,
            "sybaseSkipFullafterLogBkp": False,
            "notSynthesizeFullFromPrevBackup": False,
            "backupLevel": 2,
            "incLevel": 1,
            "adHocBackup": False,
            "runIncrementalBackup": False,
            "doNotTruncateLog": False,
            "vsaBackupOptions": {
              "backupFailedVMsOnly": False
            },
            "cdrOptions": {
              "incremental": False,
              "dataVerificationOnly": False,
              "full": True
            },
            "dataOpt": {
              "skipCatalogPhaseForSnapBackup": False,
              "useCatalogServer": True,
              "followMountPoints": True,
              "enforceTransactionLogUsage": False,
              "skipConsistencyCheck": False,
              "createNewIndex": False,
              "autoCopy": False
            },
            "distAppsBackupOptions": {
              "runLogBkp": False,
              "runDataBkp": False
            },
            "mediaOpt": {}
          },
          "adminOpts": {
            "contentIndexingOption": {
              "subClientBasedAnalytics": False
            }
          },
          "commonOpts": {
            "perfJobOpts": {}
          }
        }
      }
    ]
  }
}