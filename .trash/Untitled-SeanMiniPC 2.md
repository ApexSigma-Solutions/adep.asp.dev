<!--

Documentation: The <voice> tag value may use an identifier such as a name or email-like format (e.g., "Sean Steyn @work").

If using email-like formats, ensure downstream systems parsing <voice> support such identifiers.

-->

  

```poml

<poml>
    <task>refine</task>
    <email>
        <body>Please be advised that the following was noted this morning at Vida Old Mutual (VID1208) in Cape Town. The state of the stock being delivered, visible in the image attached is less than desirable, and the driver does not have a tablet with him to enable the EDI invoicing. Is this the reason we are having so many issues with EDI invoices not being received timeously by the stores? Why would the driver not be delivering with a tablet? Do they have sufficient tablets to cope with the demand? I would also like to understand, how come we struggle with getting EDI to work effectively over public holidays and weekends. Is this not meant to be an automated system? Do you still employ someone to push a button? </body>
	</email>
    <output>
        <tone>concerned, enquiry, professional</tone>

        <voice>Sean Steyn @work</voice>

    </output>

</poml>

```