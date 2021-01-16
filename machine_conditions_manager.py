class MachineConditionsManager:
    def __init__(self, code_generator):
        self.code_generator = code_generator

    def carry_out_condition(
        self,
        condition="",
        left_value=-1,
        left_symbol_address=-1,
        left_index_address=-1,
        left_offset=-1,
        right_value=-1,
        right_symbol_address=-1,
        right_index_address=-1,
        right_offset=-1,
    ):

        if (
            left_symbol_address != -1
            and left_index_address != -1
            and right_symbol_address != -1
            and right_index_address != -1
        ):

            self.code_generator.check_condition(
                condition=condition,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_symbol_address=right_symbol_address,
                right_index_address=right_index_address,
                right_offset=right_offset,
            )
        # tab(a) ? variable
        elif (
            left_symbol_address != -1
            and left_index_address != -1
            and right_symbol_address != -1
        ):

            self.code_generator.check_condition(
                condition=condition,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_symbol_address=right_symbol_address,
            )
        # variable ? tab(a)
        elif (
            left_symbol_address != -1
            and right_symbol_address != -1
            and right_index_address != -1
        ):

            if condition == "=" or condition == "!=":
                self.code_generator.check_condition(
                    condition=condition,
                    right_symbol_address=left_symbol_address,
                    left_symbol_address=right_symbol_address,
                    left_index_address=right_index_address,
                    left_offset=right_offset,
                )
            else:
                self.code_generator.check_condition(
                    condition=condition,
                    left_symbol_address=left_symbol_address,
                    right_symbol_address=right_symbol_address,
                    right_index_address=right_index_address,
                    right_offset=right_offset,
                )
        # tab(a) ? value
        elif (
            left_symbol_address != -1 and left_index_address != -1 and right_value != -1
        ):

            self.code_generator.check_condition(
                condition=condition,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_value=right_value,
            )
        # value ? tab(a)
        elif (
            left_value != -1
            and right_symbol_address != -1
            and right_index_address != -1
        ):

            if condition == "=" or condition == "!=":
                self.code_generator.check_condition(
                    condition=condition,
                    right_value=left_value,
                    left_symbol_address=right_symbol_address,
                    left_index_address=right_index_address,
                    left_offset=right_offset,
                )
            else:
                self.code_generator.check_condition(
                    condition=condition,
                    left_value=left_value,
                    right_symbol_address=right_symbol_address,
                    right_index_address=right_index_address,
                    right_offset=right_offset,
                )
        # variable ? variable
        elif left_symbol_address != -1 and right_symbol_address != -1:
            self.code_generator.check_condition(
                condition=condition,
                left_symbol_address=left_symbol_address,
                right_symbol_address=right_symbol_address,
            )
        # variable ? value
        elif left_symbol_address != -1 and right_value != -1:
            self.code_generator.check_condition(
                condition=condition,
                left_symbol_address=left_symbol_address,
                right_value=right_value,
            )
        # value ? variable
        elif left_value != -1 and right_symbol_address != -1:
            if condition == "=" or condition == "!=":
                self.code_generator.check_condition(
                    condition=condition,
                    left_symbol_address=right_symbol_address,
                    right_value=left_value,
                )
            else:
                self.code_generator.check_condition(
                    condition=condition,
                    left_value=left_value,
                    right_symbol_address=right_symbol_address,
                )
        elif left_value != -1 and right_value != -1:
            if condition == "=" or condition == "!=":
                self.code_generator.check_condition(
                    condition=condition, left_value=right_value, right_value=left_value
                )
            else:
                self.code_generator.check_condition(
                    condition=condition, left_value=left_value, right_value=right_value
                )
