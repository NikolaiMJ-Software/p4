from src.errors import TypeError


class ControlFlow:
    def check_while(self, node, cond_type):
        # while condition must be bool
        if cond_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"while condition must be bool, got {cond_type}"
            )
        return "bool"

    def check_dowhile(self, node, cond_type):
        # dowhile condition must be bool
        if cond_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"dowhile condition must be bool, got {cond_type}"
            )
        return "bool"

    def check_forrange(self, node, start_type, end_type):
        # Range start and end must be numeric
        if not self.is_numeric(start_type) or not self.is_numeric(end_type):
            if not self.is_numeric(start_type):
                error_node = node.start
            else:
                error_node = node.end
            raise TypeError(
                self.code,
                error_node,
                f"for-range bounds must be numeric, got {start_type} and {end_type}"
            )

    def check_foreach(self, node, collection):
        # Check if the list exists
        if collection is False:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.collection}' does not exist"
            )

        # Check if the collection is a list
        if not isinstance(collection, list):
            raise TypeError(
                self.code,
                self.value_error_node(node),
                f"Cannot iterate over non-list type '{collection}'"
            )
