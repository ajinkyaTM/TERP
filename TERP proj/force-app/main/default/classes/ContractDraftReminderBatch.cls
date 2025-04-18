global class ContractDraftReminderBatch implements Database.Batchable<sObject>{
    
    global Database.QueryLocator start(Database.BatchableContext BC) {
        // collect the batches of records or objects to be passed to execute
        
        String query = 'SELECT Id, Status, Parent_Contract__c FROM Contract WHERE Status = \'Draft\'';            
        System.debug('query of contract :-'+query);
        return Database.getQueryLocator(query);
    }
    
    global void execute(Database.BatchableContext BC, List<Contract> contractList) {
        system.debug('Inside Execute method :-'+contractList);
        List<Messaging.SingleEmailMessage> emailsToSend = new List<Messaging.SingleEmailMessage>();
        EmailTemplate emailTempExpired = [select id,name from EmailTemplate  where Name ='Child Contract New Draft Reminder' Limit 1];
        EmailTemplate emailTempNew = [select id,name from EmailTemplate  where Name ='Contract New Draft Reminder' Limit 1];
        For(Contract cont : contractList){
            if (cont.Parent_Contract__c != null) {
                // Create and populate email message
                Messaging.SingleEmailMessage email = Messaging.renderStoredEmailTemplate(emailTempNew.Id, cont.Id, cont.Id);
                //email.setTemplateId(emailTempNew.Id);
                List<String> toEmailsNew = system.label.EmailIdsForExpireContractEmailAlert.split(';');
                email.setToAddresses(toEmailsNew);
                email.setSaveAsActivity(false);
                email.setTargetObjectId(UserInfo.getUserId()); // Set the recipient of the email alert                
                
                // Add email to list
                emailsToSend.add(email);
            }
            Else if(cont.Parent_Contract__c == null){
                Messaging.SingleEmailMessage email = Messaging.renderStoredEmailTemplate(emailTempExpired.Id, cont.Id, cont.Id);
                //email.setTemplateId(emailTempExpired.Id);
                List<String> toEmailsOld = system.label.EmailIdsForExpireContractEmailAlert.split(';');
                email.setToAddresses(toEmailsOld);
                email.setSaveAsActivity(false);
                email.setTargetObjectId(UserInfo.getUserId()); // Set the recipient of the email alert                
                
                // Add email to list
                emailsToSend.add(email);
            }
        }
        // Send emails
        if (!emailsToSend.isEmpty()) {
            Messaging.sendEmail(emailsToSend);
        }
    }
    global void finish(Database.BatchableContext BC) {
        
    }
}