global class ContractExpirationReminderBatch implements Database.Batchable<sObject> {
    
    global Database.QueryLocator start(Database.BatchableContext BC) {
        // collect the batches of records or objects to be passed to execute
        Integer remainingDays = 2;
        Boolean check = false;
        System.debug('Called');
        String query = 'SELECT Id, ContractNumber, AccountId, EndDate, ContractTerm  FROM Contract WHERE Status = \'Activated\' AND Contract_Remaining_Days__c <= ' + remainingDays + ' AND Child_Contract_Created__c = ' + check;            
        System.debug('query=='+query);
        return Database.getQueryLocator(query);
    }
    
    global void execute(Database.BatchableContext BC, List<Contract> contractList) {
        System.debug('execute called');
        // process each batch of records
        try {
            //List<Contract>updateList = New List<Contract>();
            List<Contract>childContractList = New List<Contract>();
            List<Messaging.SingleEmailMessage> emailMessages = new List<Messaging.SingleEmailMessage>();
            EmailTemplate EmailTemp = [select id,name from EmailTemplate  where Name ='Contract - Reminder' Limit 1];
            System.debug('contractList==='+contractList);
            for(Contract con : contractList){
                
                con.Child_Contract_Created__c = true;
                
                Contract cont = New Contract();
                if(con.AccountId != Null){
                    cont.AccountId = con.AccountId;
                }
                cont.ContractTerm = con.ContractTerm;
                cont.StartDate = con.EndDate;
                
                cont.Parent_Contract__c = con.Id;
                childContractList.add(cont);
                
                //Messaging.SingleEmailMessage email = new Messaging.SingleEmailMessage();
                Messaging.SingleEmailMessage email = Messaging.renderStoredEmailTemplate(emailTemp.Id, con.Id, con.Id);
                List<String>toEmails = system.label.EmailIdsForExpireContractEmailAlert.split(';');
                email.setToAddresses(toEmails);
                //email.setTemplateId(emailTemp.Id);
                email.setSaveAsActivity(false);
                email.setTargetObjectId(UserInfo.getUserId());
                
                // Add the email to the list
                emailMessages.add(email);                                
            }
            System.debug('emailMessages+++'+emailMessages);
            List<Messaging.SendEmailResult> emailResults = Messaging.sendEmail(emailMessages);
            
            if(contractList.Size()>0){
                System.debug('contractList+++'+contractList);
                Update contractList;
            }
            if(childContractList.Size()>0){
                System.debug('childContractList>>>>'+childContractList);
                Insert childContractList;
            }
        } catch(Exception e) {
            System.debug(e);
        }
        
    }   
    
    global void finish(Database.BatchableContext BC) {
        // execute any post-processing operations
    }
}