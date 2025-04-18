trigger ContactAddressSync on Contact (before insert, before update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            ContactAddressHandler.populateMailingAddress(Trigger.new, null);
        } else if (Trigger.isUpdate) {
            ContactAddressHandler.populateMailingAddress(Trigger.new, Trigger.oldMap);
        }
    }
}