@isTest
public class ContractExpirationReminderBatch_Test {

    @testSetup
    public static void setupData(){
        Account acc = testDataFactory.createAccount();
        Insert acc;
        Contract contr1 = testDataFactory.createContract(acc.Id, Null,'Draft');
        Insert contr1;
        /*Contract contr2 = testDataFactory.createContract(acc.Id, contr1.Id,'Activated');
        Insert contr2;*/
    }
    @isTest
    static void testContractExpireReminder() {
        
        Contract contr = [SELECT Id, ContractNumber, AccountId, EndDate, ContractTerm  FROM Contract];
        contr.Status = 'Activated';
        Update contr;
        
        Test.startTest();
        ContractExpirationReminderBatch batchJob = new ContractExpirationReminderBatch();
        Database.executeBatch(batchJob);
        Test.stopTest();

    }
    @isTest
    static void testContractExpireReminderScheduler() {
        
        Test.startTest();
        
        //String cronExp = '0 0 0 15 3 ? 2024';
        String cronExp = '0 0 0 15 3 ? 2026';
        ContractExpirationScheduler scheduler = new ContractExpirationScheduler();
        String jobId = System.schedule('Test Contract Expiration Scheduler', cronExp, scheduler);
        
        Test.stopTest();

        System.assertNotEquals(null, jobId);
    }
}