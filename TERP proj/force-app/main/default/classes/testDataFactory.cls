@isTest
public class testDataFactory {

    public static Account createAccount(){
        Account acc = new Account();
        acc.Name = 'Test Account';
        acc.Type = 'Customer';
        
        Return acc;
    }
    public static Contract createContract(Id accId, Id parentId, String status){
        Contract contr = new Contract();
        contr.AccountId = accId;
        contr.Status = status;
        contr.StartDate = Date.today().addDays(-30);
        contr.ContractTerm = 1;
        contr.Parent_Contract__c = parentId;
        contr.Child_Contract_Created__c = False;
        
        Return contr;
    }
}