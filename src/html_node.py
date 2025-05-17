   
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Child classes must implement this method")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        html_props = ""
        for key, value in self.props.items():
            html_props += f' {key}="{value}"'
        
        return html_props
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def pretty_print(self, indent=0):
        ind = "  " * indent
        print(f"{ind}{self.tag}, props={self.props}, value={self.value}'")
        for child in self.children or []:
            child.pretty_print(indent + 1)


class LeafNode(HTMLNode):
    def __init__(self, tag,  value,  props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

