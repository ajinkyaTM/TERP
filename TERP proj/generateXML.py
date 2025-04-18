import os
import argparse
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom

SRC_FOLDER = "force-app/main/default"

# Mapping of folder names to Metadata types for package.xml
FOLDER_TO_METADATA_TYPE = {
    "installedPackages": "InstalledPackage",
    "marketingappextensions": "MarketingAppExtension",
    "labels": "CustomLabels",
    "staticresources": "StaticResource",
    "scontrols": "Scontrol",
    "certs": "Certificate",
    "messageChannels": "LightningMessageChannel",
    "lwc": "LightningComponentBundle",
    "aura": "AuraDefinitionBundle",
    "components": "ApexComponent",
    "pages": "ApexPage",
    "queues": "Queue",
    "CaseSubjectParticles": "CaseSubjectParticle",
    "inboundNetworkConnections": "InboundNetworkConnection",
    "outboundNetworkConnections": "OutboundNetworkConnection",
    "externalAuthIdentityProviders": "ExternalAuthIdentityProvider",
    "externalCredentials": "ExternalCredential",
    "namedCredentials": "NamedCredential",
    "dataSources": "ExternalDataSource",
    "externalServiceRegistrations": "ExternalServiceRegistration",
    "roles": "Role",
    "groups": "Group",
    "globalValueSets": "GlobalValueSet",
    "standardValueSets": "StandardValueSet",
    "customPermissions": "CustomPermission",
    "objects": "CustomObject",
    "reportTypes": "ReportType",
    "reports": "Report",
    "dashboards": "Dashboard",
    "analyticSnapshots": "AnalyticSnapshot",
    "feedFilters": "CustomFeedFilter",
    "layouts": "Layout",
    "documents": "Document",
    "weblinks": "CustomPageWebLink",
    "letterhead": "Letterhead",
    "email": "EmailTemplate",
    "quickActions": "QuickAction",
    "uiFormatSpecificationSets": "UiFormatSpecificationSet",
    "flexipages": "FlexiPage",
    "tabs": "CustomTab",
    "customApplicationComponents": "CustomApplicationComponent",
    "applications": "CustomApplication",
    "customMetadata": "CustomMetadata",
    "flows": "Flow",
    "flowDefinitions": "FlowDefinition",
    "flowtests": "FlowTest",
    "processflowmigrations": "ProcessFlowMigration",
    "contentassets": "ContentAsset",
    "workflows": "Workflow",
    "assignmentRules": "AssignmentRules",
    "autoResponseRules": "AutoResponseRules",
    "escalationRules": "EscalationRules",
    "postTemplates": "PostTemplate",
    "approvalProcesses": "ApprovalProcess",
    "homePageComponents": "HomePageComponent",
    "homePageLayouts": "HomePageLayout",
    "objectTranslations": "CustomObjectTranslation",
    "globalValueSetTranslations": "GlobalValueSetTranslation",
    "standardValueSetTranslations": "StandardValueSetTranslation",
    "dw": "DataWeaveResource",
    "classes": "ApexClass",
    "triggers": "ApexTrigger",
    "testSuites": "ApexTestSuite",
    "profiles": "Profile",
    "permissionsets": "PermissionSet",
    "mutingpermissionsets": "MutingPermissionSet",
    "permissionsetgroups": "PermissionSetGroup",
    "profilePasswordPolicies": "ProfilePasswordPolicy",
    "profileSessionSettings": "ProfileSessionSetting",
    "myDomainDiscoverableLogins": "MyDomainDiscoverableLogin",
    "blacklistedConsumers": "BlacklistedConsumer",
    "oauthcustomscopes": "OauthCustomScope",
    "oauthtokenexchangehandlers": "OauthTokenExchangeHandler",
    "userProvisioningConfigs": "UserProvisioningConfig",
    "notificationtypes": "CustomNotificationType",
    "externalClientApps": "ExternalClientApplication",
    "extlClntAppOauthSettings": "ExtlClntAppOauthSettings",
    "extlClntAppGlobalOauthSets": "ExtlClntAppGlobalOauthSettings",
    "extlClntAppOauthPolicies": "ExtlClntAppOauthConfigurablePolicies",
    "extlClntAppPolicies": "ExtlClntAppConfigurablePolicies",
    "extlClntAppSamlConfigurablePolicies": "ExtlClntAppSamlConfigurablePolicies",
    "datacategorygroups": "DataCategoryGroup",
    "remoteSiteSettings": "RemoteSiteSetting",
    "cspTrustedSites": "CspTrustedSite",
    "redirectWhitelistUrls": "RedirectWhitelistUrl",
    "matchingRules": "MatchingRules",
    "duplicateRules": "DuplicateRule",
    "cleanDataServices": "CleanDataService",
    "customindex": "CustomIndex",
    "authproviders": "AuthProvider",
    "eclair": "EclairGeoData",
    "wave": "WaveAnalyticAssetCollection",
    "analyticsWorkspaces": "AnalyticsWorkspace",
    "appTemplates": "AppFrameworkTemplateBundle",
    "IPAddressRanges": "IPAddressRange",
    "recordAlertCategories": "RecordAlertCategory",
    "apexEmailNotifications": "ApexEmailNotifications",
    "channelLayouts": "ChannelLayout",
    "sites": "CustomSite",
    "briefcaseDefinitions": "BriefcaseDefinition",
    "sharingRules": "SharingRules",
    "iframeWhiteListUrlSettings": "IframeWhiteListUrlSettings",
    "communities": "Community",
    "ChatterExtensions": "ChatterExtension",
    "decisionTables": "DecisionTable",
    "decisionTableDatasetLinks": "DecisionTableDatasetLink",
    "aiApplications": "AIApplication",
    "aiApplicationConfigs": "AIApplicationConfig",
    "mlPredictions": "MLPredictionDefinition",
    "mlRecommendations": "MLRecommendationDefinition",
    "mlDataDefinitions": "MLDataDefinition",
    "batchProcessJobDefinitions": "BatchProcessJobDefinition",
    "expressionSetMessageToken": "ExpressionSetMessageToken",
    "ExplainabilityMsgTemplates": "ExplainabilityMsgTemplate",
    "expressionSetObjectAlias": "ExpressionSetObjectAlias",
    "decisionMatrixDefinition": "DecisionMatrixDefinition",
    "decisionMatrixVersion": "DecisionMatrixDefinitionVersion",
    "expressionSetDefinition": "ExpressionSetDefinition",
    "expressionSetVersion": "ExpressionSetDefinitionVersion",
    "externalAIModels": "ExternalAIModel",
    "serviceAISetupDescriptions": "ServiceAISetupDefinition",
    "serviceAISetupFields": "ServiceAISetupField",
    "platformEventChannels": "PlatformEventChannel",
    "platformEventChannelMembers": "PlatformEventChannelMember",
    "eventRelays": "EventRelayConfig",
    "managedEventSubscriptions": "ManagedEventSubscription",
    "integrationProviderDefinitions": "IntegrationProviderDef",
    "callCenters": "CallCenter",
    "milestoneTypes": "MilestoneType",
    "entitlementProcesses": "EntitlementProcess",
    "entitlementTemplates": "EntitlementTemplate",
    "PublicKeyCertificate": "PublicKeyCertificate",
    "PublicKeyCertificateSet": "PublicKeyCertificateSet",
    "messagingChannels": "MessagingChannel",
    "Canvases": "CanvasMetadata",
    "MobileApplicationDetails": "MobileApplicationDetail",
    "connectedApps": "ConnectedApp",
    "appMenus": "AppMenu",
    "notificationTypeConfig": "NotificationTypeConfig",
    "delegateGroups": "DelegateGroup",
    "brandingSets": "BrandingSet",
    "managedContentTypes": "ManagedContentType",
    "experiencePropertyTypeBundles": "ExperiencePropertyTypeBundle",
    "digitalExperiences": "DigitalExperienceBundle",
    "siteDotComSites": "SiteDotCom",
    "experienceContainers": "ExperienceContainer",
    "networkBranding": "NetworkBranding",
    "flowCategories": "FlowCategory",
    "lightningBolts": "LightningBolt",
    "lightningExperienceThemes": "LightningExperienceTheme",
    "lightningOnboardingConfigs": "LightningOnboardingConfig",
    "customHelpMenuSections": "CustomHelpMenuSection",
    "prompts": "Prompt",
    "samlssoconfigs": "SamlSsoConfig",
    "corsWhitelistOrigins": "CorsWhitelistOrigin",
    "actionLinkGroupTemplates": "ActionLinkGroupTemplate",
    "conversationMessageDefinitions": "ConversationMessageDefinition",
    "synonymDictionaries": "SynonymDictionary",
    "pathAssistants": "PathAssistant",
    "animationRules": "AnimationRule",
    "LeadConvertSettings": "LeadConvertSettings",
    "liveChatSensitiveDataRule": "LiveChatSensitiveDataRule",
    "cachePartitions": "PlatformCachePartition",
    "topicsForObjects": "TopicsForObjects",
    "restrictionRules": "RestrictionRule",
    "fieldRestrictionRules": "FieldRestrictionRule",
    "recommendationStrategies": "RecommendationStrategy",
    "emailservices": "EmailServicesFunction",
    "ActionLauncherItemDef": "ActionLauncherItemDef",
    "recordActionDeployments": "RecordActionDeployment",
    "BusinessProcessTypeDefinitions": "BusinessProcessTypeDefinition",
    "ApplicationSubtypeDefinitions": "ApplicationSubtypeDefinition",
    "ExplainabilityActionDefinitions": "ExplainabilityActionDefinition",
    "ExplainabilityActionVersions": "ExplainabilityActionVersion",
    "ChoiceList": "ChoiceList",
    "EmbeddedServiceConfig": "EmbeddedServiceConfig",
    "EmbeddedServiceBranding": "EmbeddedServiceBranding",
    "EmbeddedServiceFlowConfig": "EmbeddedServiceFlowConfig",
    "EmbeddedServiceMenuSettings": "EmbeddedServiceMenuSettings",
    "callCoachingMediaProviders": "CallCoachingMediaProvider",
    "actionPlanTemplates": "ActionPlanTemplate",
    "timelineObjectDefinitions": "TimelineObjectDefinition",
    "ConvIntelligenceSignalRule": "ConvIntelligenceSignalRule",
    "searchCustomizations": "SearchCustomization",
    "searchOrgWideConfiguration": "SearchOrgWideObjectConfig",
    "PlatformEventSubscriberConfigs": "PlatformEventSubscriberConfig",
    "pipelineInspMetricConfigs": "PipelineInspMetricConfig",
    "recordAlertDataSources": "RecordAlertDataSource",
    "recAlrtDataSrcExpSetDefs": "RecAlrtDataSrcExpSetDef",
    "recordAlertTemplates": "RecordAlertTemplate",
    "settings": "Settings"
}

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_changed_labels(base_branch, head_ref):
    diff_command = f"git diff {base_branch}..{head_ref} -- {SRC_FOLDER}/labels/CustomLabels.labels-meta.xml"
    result = subprocess.run(diff_command, shell=True, capture_output=True, text=True)
    print(f"Result of git diff command for lables:\n{result.stdout}")
    added_labels = []
    deleted_labels = []

    for line in result.stdout.splitlines():
        line = line.strip()
        if "<fullName>" in line:
            label_name = line.replace("<fullName>", "").replace("</fullName>", "").strip("+- ").strip()
            if line.startswith("+"):
                added_labels.append(label_name)
            elif line.startswith("-"):
                deleted_labels.append(label_name)

    print(f"Added labels: {added_labels}")
    print(f"Deleted labels: {deleted_labels}")

    return added_labels, deleted_labels

def get_diff_files(base_branch, head_ref):
    diff_command = f"git diff --name-status {base_branch}..{head_ref}"
    print(f"Running command: {diff_command}")
    result = subprocess.run(diff_command, shell=True, capture_output=True, text=True)
    print(f"Result of git diff command:\n{result.stdout}")

    created_or_modified = {}
    deleted = {}

    label_checked = False  # Only run label diff once

    for line in result.stdout.splitlines():
        parts = line.split('\t')
        status = parts[0]

        # Handle renamed files
        if status.startswith('R') and len(parts) == 3:
            _, old_path, new_path = parts
            paths = [(old_path, deleted), (new_path, created_or_modified)]
        else:
            file_path = parts[1] if len(parts) > 1 else None
            if not file_path:
                continue
            paths = [(file_path, deleted if status == 'D' else created_or_modified)]

        for path, target_dict in paths:
            if not path.startswith(SRC_FOLDER):
                continue

            parts = path.split('/')
            if len(parts) < 5:
                continue

            folder_name = parts[3]
            metadata_type = FOLDER_TO_METADATA_TYPE.get(folder_name)
            if not metadata_type:
                continue

            # Handle Custom Labels (only once)
            if folder_name == "labels" and not label_checked:
                added_labels, deleted_labels = get_changed_labels(base_branch, head_ref)
                if added_labels:
                    created_or_modified.setdefault("CustomLabel", []).extend(added_labels)
                if deleted_labels:
                    deleted.setdefault("CustomLabel", []).extend(deleted_labels)
                label_checked = True
                continue

            # Handle nested metadata inside objects
            if folder_name == "objects" and len(parts) >= 6:
                object_name = parts[4]
                sub_folder_or_file = parts[5]

                if sub_folder_or_file == "fields" and len(parts) >= 7:
                    field_file = parts[6]
                    field_name = field_file.split('.')[0]
                    metadata_name = f"{object_name}.{field_name}"
                    target_dict.setdefault("CustomField", []).append(metadata_name)
                else:
                    file_name = parts[5]
                    metadata_name = file_name.split('.')[0]
                    target_dict.setdefault(metadata_type, []).append(metadata_name)

            # Handle Custom Index 
            elif folder_name == "customindex" and len(parts) >= 5:
                index_file = parts[4]
                name_parts = index_file.split('.')[0].split('-')
                object_name, index_name = index_file.split('.')[0], index_file.split('.')[1]
                metadata_name = f"{object_name}.{index_name}"
                target_dict.setdefault("CustomIndex", []).append(metadata_name)

            else:
                file_name = parts[4]

                if folder_name == "staticresources":
                    # Handle .resource-meta.xml and .zip files
                    if file_name.endswith(".resource-meta.xml"):
                        metadata_name = file_name.replace(".resource-meta.xml", "")
                    elif file_name.endswith(".zip"):
                        metadata_name = file_name.replace(".zip", "")
                    else:
                        # If it's an asset file like .js/.png, infer the resource name from folder structure
                        if len(parts) >= 6:
                            metadata_name = parts[4]  # folder name is the resource
                        else:
                            metadata_name = file_name.split('.')[0]
                else:
                    metadata_name = file_name.split('.')[0]

                target_dict.setdefault(metadata_type, []).append(metadata_name)

    return created_or_modified, deleted

def create_package_xml(added_or_modified_files):
    package = ET.Element("Package", xmlns="http://soap.sforce.com/2006/04/metadata")
    for metadata_type, files in added_or_modified_files.items():
        types_element = ET.SubElement(package, "types")
        for file in sorted(set(files)):
            member = ET.SubElement(types_element, "members")
            member.text = file
        name = ET.SubElement(types_element, "name")
        name.text = metadata_type

    version = ET.SubElement(package, "version")
    version.text = "60.0"

    with open("package.xml", "w", encoding="utf-8") as f:
        f.write(prettify_xml(package))

def create_destructive_changes_xml(deleted_files):
    destructive_changes = ET.Element("Package", xmlns="http://soap.sforce.com/2006/04/metadata")
    for metadata_type, files in deleted_files.items():
        types_element = ET.SubElement(destructive_changes, "types")
        for file in sorted(set(files)):
            member = ET.SubElement(types_element, "members")
            member.text = file
        name = ET.SubElement(types_element, "name")
        name.text = metadata_type

    version = ET.SubElement(destructive_changes, "version")
    version.text = "60.0"

    with open("destructiveChanges.xml", "w", encoding="utf-8") as f:
        f.write(prettify_xml(destructive_changes))

def generate_metadata_files(base_branch, head_ref):
    print(f"Comparing branches {base_branch} and {head_ref}...")
    added_or_modified_files, deleted_files = get_diff_files(base_branch, head_ref)

    if not added_or_modified_files and not deleted_files:
        print(f"No changes found between {base_branch} and {head_ref}.")
        return

    create_package_xml(added_or_modified_files)
    create_destructive_changes_xml(deleted_files)
    print("Generated package.xml and destructiveChanges.xml successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate package.xml and destructiveChanges.xml by comparing branches.")
    parser.add_argument("--base_branch", help="The base branch to compare against.")
    parser.add_argument("--compare_branch", help="The branch to compare with the base branch.")
    parser.add_argument("--base_commit", help="The base commit to compare against (for push/merge events).")
    parser.add_argument("--head_commit", help="The head commit to compare with (for push/merge events).")
    args = parser.parse_args()

    # Determine comparison strategy
    if args.base_branch and args.compare_branch:
        base_branch = args.base_branch
        compare_branch = args.compare_branch
        print(f"Comparing branches: {base_branch}..{compare_branch}")
        generate_metadata_files(base_branch, compare_branch)
    elif args.base_commit and args.head_commit:
        base_commit = args.base_commit
        head_commit = args.head_commit
        print(f"Comparing commits: {base_commit}..{head_commit}")
        generate_metadata_files(base_commit, head_commit)
    else:
        print("Error: Either base_branch and compare_branch OR base_commit and head_commit must be provided.")
        exit(1)