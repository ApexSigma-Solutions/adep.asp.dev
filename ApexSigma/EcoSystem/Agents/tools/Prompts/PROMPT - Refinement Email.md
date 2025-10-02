# PROMPT - Refinement Email 
<!--
Documentation: The <voice> tag value may use an identifier such as a name or email-like format (e.g., "Sean Steyn @work").If using email-like formats, ensure downstream systems parsing <voice> support such identifiers.
-->

```poml
<poml>
    <task>"the instruction"</task>
    <email>
        <body>"place then body of the email you want to refine here"</body>
	</email>
    <output>
        <tone>concerned, enquiry, professional</tone>
        <voice>Sean Steyn @work</voice>
    </output>
</poml>
```