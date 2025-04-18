@isTest
public class ContactAddressHandlerTest {

    /*@isTest
    static void testPopulateMailingAddress_BasicPopulation() {
        // Create Account
        Account acc = new Account(
            Name = 'Test Account',
            BillingStreet = '123 Main St',
            BillingCity = 'Sample City',
            BillingState = 'CA',
            BillingPostalCode = '90001',
            BillingCountry = 'USA'
        );
        insert acc;

        // Create Contact with no mailing address
        Contact con = new Contact(
            FirstName = 'John',
            LastName = 'Doe',
            AccountId = acc.Id
        );
        insert con;

        // Simulate trigger context
        List<Contact> newContacts = [SELECT Id, AccountId, MailingStreet, MailingCity, MailingState, MailingPostalCode, MailingCountry FROM Contact WHERE Id = :con.Id];
        Map<Id, Contact> oldMap = new Map<Id, Contact>();

        Test.startTest();
        ContactAddressHandler.populateMailingAddress(newContacts, oldMap);
        Test.stopTest();

        Contact updatedCon = newContacts[0];
        System.assertEquals('123 Main St', updatedCon.MailingStreet);
        System.assertEquals('Sample City', updatedCon.MailingCity);
        System.assertEquals('CA', updatedCon.MailingState);
        System.assertEquals('90001', updatedCon.MailingPostalCode);
        System.assertEquals('USA', updatedCon.MailingCountry);
    }*/

    @isTest
    static void testPopulateMailingAddress_WithOldMap() {
        // Create two Accounts
        Account acc1 = new Account(Name = 'Account A', BillingStreet = 'Street A', BillingCity = 'City A', BillingState = 'State A', BillingPostalCode = '11111', BillingCountry = 'Country A');
        Account acc2 = new Account(Name = 'Account B', BillingStreet = 'Street B', BillingCity = 'City B', BillingState = 'State B', BillingPostalCode = '22222', BillingCountry = 'Country B');
        insert new List<Account>{acc1, acc2};

        // Create Contact under acc1
        Contact con = new Contact(FirstName = 'Jane', LastName = 'Smith', AccountId = acc1.Id);
        insert con;

        // Simulate update: move Contact to acc2
        Contact updatedCon = new Contact(Id = con.Id, AccountId = acc2.Id);
        List<Contact> newContacts = new List<Contact>{updatedCon};

        // Simulate oldMap
        Map<Id, Contact> oldMap = new Map<Id, Contact>{
            con.Id => con
        };

        Test.startTest();
        ContactAddressHandler.populateMailingAddress(newContacts, oldMap);
        Test.stopTest();

        Contact resultCon = newContacts[0];
        System.assertEquals('Street B', resultCon.MailingStreet);
        System.assertEquals('City B', resultCon.MailingCity);
        System.assertEquals('State B', resultCon.MailingState);
        System.assertEquals('22222', resultCon.MailingPostalCode);
        System.assertEquals('Country B', resultCon.MailingCountry);
    }

    @isTest
    static void testPopulateMailingAddress_NoAccount() {
        Contact con = new Contact(FirstName = 'No', LastName = 'Account');
        insert con;

        List<Contact> newContacts = [SELECT Id, AccountId, MailingStreet, MailingCity, MailingState, MailingPostalCode, MailingCountry FROM Contact WHERE Id = :con.Id];
        Map<Id, Contact> oldMap = new Map<Id, Contact>();

        Test.startTest();
        ContactAddressHandler.populateMailingAddress(newContacts, oldMap);
        Test.stopTest();

        // Since no AccountId, nothing should be populated
        Contact untouchedCon = newContacts[0];
        System.assert(String.isBlank(untouchedCon.MailingStreet));
    }
    @isTest
    static void testIsMailingAddressEmpty_DirectCall() {
        Contact blankCon = new Contact();
        System.assert(ContactAddressHandler.isMailingAddressEmpty(blankCon), 'Expected true for empty contact');
    
        Contact filledCon = new Contact(MailingStreet='123 A St');
        System.assert(!ContactAddressHandler.isMailingAddressEmpty(filledCon), 'Expected false for partially filled contact');
    }
}