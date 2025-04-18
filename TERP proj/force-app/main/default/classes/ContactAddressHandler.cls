public class ContactAddressHandler {

    public static void populateMailingAddress(List<Contact> newContacts, Map<Id, Contact> oldMap) {
        Set<Id> accountIds = new Set<Id>();

        for (Contact con : newContacts) {
            if (con.AccountId != null) {
                if (oldMap == null || con.AccountId != oldMap.get(con.Id).AccountId ||
                    isMailingAddressEmpty(con)) {
                    accountIds.add(con.AccountId);
                }
            }
        }

        if (accountIds.isEmpty()) return;

        Map<Id, Account> accMap = new Map<Id, Account>(
            [SELECT Id, BillingStreet, BillingCity, BillingState, BillingPostalCode, BillingCountry
             FROM Account WHERE Id IN :accountIds]
        );

        for (Contact con : newContacts) {
            if (con.AccountId != null && accMap.containsKey(con.AccountId)) {
                Account acc = accMap.get(con.AccountId);
                con.MailingStreet     = acc.BillingStreet;
                con.MailingCity       = acc.BillingCity;
                con.MailingState      = acc.BillingState;
                con.MailingPostalCode = acc.BillingPostalCode;
                con.MailingCountry    = acc.BillingCountry;
            }
        }
    }
	@TestVisible
    private static Boolean isMailingAddressEmpty(Contact con) {
        return String.isBlank(con.MailingStreet) &&
               String.isBlank(con.MailingCity) &&
               String.isBlank(con.MailingState) &&
               String.isBlank(con.MailingPostalCode) &&
               String.isBlank(con.MailingCountry);
    }
}