global class ContractDraftScheduler implements Schedulable{

    global void execute(SchedulableContext SC) {
        ContractDraftReminderBatch batchDraftReminder = New ContractDraftReminderBatch();
        Database.executebatch(batchDraftReminder);
    }
}