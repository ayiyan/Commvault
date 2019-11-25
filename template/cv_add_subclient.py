SubClient = {
	"CLMP" : {
		"subClientProperties": {
			"subClientEntity": {
				"clientName": "",
				"appName": "File System",
				"backupsetName": "DefaultBackupset",
				"subclientName": "SC_CLMP"
			},
			"contentOperationType": "ADD",
			"content": [
				{
					"path": "/NasBackup/CLMP"
				}
			],
			"commonProperties": {
				"description":"CLMP backup subclient",
				"storageDevice": {
					"dataBackupStoragePolicy": {
						"storagePolicyName": ""
					}
				}
			}
		}
	},
	"ECM" : {
		"subClientProperties": {
			"subClientEntity": {
				"clientName": "",
				"appName": "File System",
				"backupsetName": "DefaultBackupset",
				"subclientName": "SC_ECM"
			},
			"contentOperationType": "ADD",
			"content": [
				{
					"path": "/NasBackup/ECM/ACTMQ"
				},
				{
					"path": "/NasBackup/ECM/EXPORT"
				},
				{
					"path": "/NasBackup/ECM/UPLOAD"
				}
			],
			"commonProperties": {
				"description":"ECM backup subclient",
				"storageDevice": {
					"dataBackupStoragePolicy": {
						"storagePolicyName": ""
					}
				}
			}
		}
	},
	"StagingArea" : {
		"subClientProperties": {
			"subClientEntity": {
				"clientName": "",
				"appName": "File System",
				"backupsetName": "DefaultBackupset",
				"subclientName": "SC_STAGING_AREA"
			},
			"contentOperationType": "ADD",
			"content": [
				{
					"path": "/StagingArea"
				}
			],
			"commonProperties": {
				"description":"StagingArea backup subclient",
				"storageDevice": {
					"dataBackupStoragePolicy": {
						"storagePolicyName": ""
					}
				}
			}
		}
	}
}