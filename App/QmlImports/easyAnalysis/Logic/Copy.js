function copyButton(from, to) {
    to.x = from.x
    to.y = from.y
    to.width = from.width
    to.height = from.height
    to.text = from.text
    to.icon.source = from.icon.source
    to.highlighted = from.highlighted

    to.ToolTip.text = ""
    //to.onClicked = from.onClicked
    //to.enabled = false
    //to.onPressed = from.onPressed
}
