@isTest
public class ContractDraftReminderBatch_Test {
    
    @testSetup
    public static void setupData(){
        Account acc = testDataFactory.createAccount();
        Insert acc;
        Contract contr1 = testDataFactory.createContract(acc.Id, Null, 'Draft');
        Insert contr1;
        Contract contr2 = testDataFactory.createContract(acc.Id, contr1.Id, 'Draft');
        Insert contr2;
    }
    @isTest
    static void testContractDraftReminder() {
        
        Test.startTest();
        ContractDraftReminderBatch batchJob = new ContractDraftReminderBatch();
        Database.executeBatch(batchJob);
        Test.stopTest();

    }
    @isTest
    static void testContractDraftReminderScheduler() {
        
        Test.startTest();
        
        //String cronExp = '0 0 0 15 3 ? 2024';
        String cronExp = '0 0 0 15 3 ? 2026';
        ContractDraftScheduler scheduler = new ContractDraftScheduler();
        String jobId = System.schedule('Test Contract Draft Scheduler', cronExp, scheduler);
        
        Test.stopTest();

        System.assertNotEquals(null, jobId);
    }
}