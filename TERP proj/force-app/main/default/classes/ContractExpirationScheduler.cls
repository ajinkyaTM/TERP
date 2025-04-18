global class ContractExpirationScheduler implements Schedulable {
    global void execute(SchedulableContext SC) {
        ContractExpirationReminderBatch batch = New ContractExpirationReminderBatch();
        Database.executebatch(batch);
    }
}