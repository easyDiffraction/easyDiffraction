function highlightCifSyntax(str)
{
    return str
        .replace(/\n(_[\w,-]+) /ig, "\n<font color=#2380b5>$1</font> ") // colorize individual keys (with space at the end), e.g., "_setup_wavelength"
        .replace(/\n(_[\w,-]+)/ig, "\n<font color=#669431>$1</font>")   // colorize keys inside loops (with new line at the end), e.g., "_phase_label"
        .replace(/loop_/ig, "<font color=#888>loop_</font>")            // colorize "loop_"
        .replace(/data_\w+/ig, "<font color=#b95e39>$&</font>")         // colorize datablock, e.g., "data_Fe3O4"
        .replace(/(\r\n|\r|\n)/ig, "<br />")                            // change newline and carriage return escape sequences to html format
}

function removeHtmlTags(html)
{
    // regex tester: https://regexr.com/
    return html
        .replace(/(\r\n|\r|\n)/ig, "")      // remove newline and carriage return escape sequences
        .replace(/<br \/>/ig, "\n")         // convert newline from html format to escape sequences
        .replace(/<style.+style>/ig, "")    // remove html style group
        .replace(/<\/?[^>]+>/ig, "")        // remove html tags
}
