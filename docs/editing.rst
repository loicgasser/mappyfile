Keys need to have matching apostrophes for now. 

    md = mymap["web"]["metadata"]
    title = "Héllo"
    md['"ows_title"'] = unicode(title, "utf-8") # need to convert to unicode


Expressions should be wrapped in brackets



Error Checking

+ Layer type not set