class MachineController:
    def __init__(
        self,
        machine_math_manager,
        machine_conditions_manager,
        assignment_manager,
        code_generator,
    ):
        self.machine_math_manager = machine_math_manager
        self.machine_conditions_manager = machine_conditions_manager
        self.assignment_manager = assignment_manager
        self.code_generator = code_generator
        self.tab_indexes = []
        self.last_read_symbols = []
        self.machine_values = []
        self.symbols = []

    def update_stack_values(
        self, tab_indexes, last_read_symbols, machine_values, symbols
    ):
        self.tab_indexes = tab_indexes
        self.last_read_symbols = last_read_symbols
        self.machine_values = machine_values
        self.symbols = symbols

    def prepare_values_for_machine_task(
        self,
        task="",
        task_value="",
        loop_type="",
        iterator_address=-1,
        left_symbol_address=-1,
        left_value=-1,
        right_symbol_address=-1,
        right_value=-1,
    ):
        left_is_var = False
        right_is_var = False

        if left_symbol_address != -1:
            left_is_var = True
        if right_symbol_address != -1:
            right_is_var = True

        if left_is_var:
            left_symbol = self.get_symbol_by_name(self.machine_values[0])
            left_symbol_address = left_symbol.get_address()

            if left_symbol.is_tab:
                left_offset = -1

                if right_is_var:
                    right_symbol = self.get_symbol_by_name(self.machine_values[1])
                    right_symbol_address = right_symbol.get_address()
                    # tab(a) [?] tab(b)
                    if right_symbol.is_tab:
                        right_index = self.tab_indexes.pop()
                        left_index = self.tab_indexes.pop()

                        right_offset = -1

                        if right_index == -1:
                            right_index_address = self.get_symbol_by_name(
                                self.last_read_symbols.pop()
                            ).get_address()
                            right_offset = right_symbol.get_tab_offset()
                        else:
                            right_index_address = 0
                            right_symbol_address += (
                                right_index - right_symbol.get_tab_offset()
                            )

                        if left_index == -1:
                            left_index_address = self.get_symbol_by_name(
                                self.last_read_symbols.pop()
                            ).get_address()
                            left_offset = left_symbol.get_tab_offset()
                        else:
                            left_index_address = 0
                            left_symbol_address += (
                                left_index - left_symbol.get_tab_offset()
                            )

                            if task == "assignment" and right_index != -1:
                                right_value = right_symbol.get_tab_symbol_value(
                                    right_index
                                )
                                if right_value == -1:
                                    left_symbol.set_tab_symbol_value_at_index(
                                        -1, left_index
                                    )
                                else:
                                    left_symbol.set_tab_symbol_value_at_index(
                                        right_value, left_index
                                    )

                        self.pass_task_to_machine(
                            task=task,
                            task_value=task_value,
                            loop_type=loop_type,
                            iterator_address=iterator_address,
                            left_symbol_address=left_symbol_address,
                            left_index_address=left_index_address,
                            left_offset=left_offset,
                            right_symbol_address=right_symbol_address,
                            right_index_address=right_index_address,
                            right_offset=right_offset,
                        )
                    # tab(a) [?] variable
                    else:
                        left_index = self.tab_indexes.pop()

                        if left_index == -1:
                            left_index_address = self.get_symbol_by_name(
                                self.last_read_symbols.pop()
                            ).get_address()
                            left_offset = left_symbol.get_tab_offset()
                        else:
                            left_index_address = 0
                            left_symbol_address += (
                                left_index - left_symbol.get_tab_offset()
                            )

                            if task == "assignment":
                                right_value = right_symbol.get_symbol_value()
                                if right_value == -1:
                                    left_symbol.set_tab_symbol_value_at_index(
                                        -1, left_index
                                    )
                                else:
                                    left_symbol.set_tab_symbol_value_at_index(
                                        right_value, left_index
                                    )

                        self.pass_task_to_machine(
                            task=task,
                            task_value=task_value,
                            loop_type=loop_type,
                            iterator_address=iterator_address,
                            left_symbol_address=left_symbol_address,
                            left_index_address=left_index_address,
                            left_offset=left_offset,
                            right_symbol_address=right_symbol_address,
                        )

                # tab(a) [?] value
                else:
                    left_index = self.tab_indexes.pop()
                    left_offset = -1

                    if left_index == -1:
                        left_index_address = self.get_symbol_by_name(
                            self.last_read_symbols.pop()
                        ).get_address()
                        left_offset = left_symbol.get_tab_offset()
                    else:
                        left_index_address = 0
                        left_symbol_address += left_index - left_symbol.get_tab_offset()

                    right_value = self.machine_values[1]

                    if task == "assignment" and left_index != -1:
                        left_symbol.set_tab_symbol_value_at_index(
                            right_value, left_index
                        )

                    self.pass_task_to_machine(
                        task=task,
                        task_value=task_value,
                        loop_type=loop_type,
                        iterator_address=iterator_address,
                        left_symbol_address=left_symbol_address,
                        left_index_address=left_index_address,
                        left_offset=left_offset,
                        right_value=right_value,
                    )
            else:
                if right_is_var:
                    right_symbol = self.get_symbol_by_name(self.machine_values[1])
                    right_symbol_address = right_symbol.get_address()

                    # variable [?] tab(i)
                    if right_symbol.is_tab:
                        right_index = self.tab_indexes.pop()
                        right_offset = -1

                        if right_index == -1:
                            right_index_address = self.get_symbol_by_name(
                                self.last_read_symbols.pop()
                            ).get_address()
                            right_offset = right_symbol.get_tab_offset()
                        else:
                            right_index_address = 0
                            right_symbol_address += (
                                right_index - right_symbol.get_tab_offset()
                            )

                        if task == "assignment":
                            if right_index == -1:
                                left_symbol.set_value(-1)
                            else:
                                right_value = right_symbol.get_tab_symbol_value(
                                    right_index
                                )
                                if right_value == -1:
                                    left_symbol.set_value(-1)
                                else:
                                    left_symbol.set_value(right_value)

                        self.pass_task_to_machine(
                            task=task,
                            task_value=task_value,
                            loop_type=loop_type,
                            iterator_address=iterator_address,
                            left_symbol_address=left_symbol_address,
                            right_symbol_address=right_symbol_address,
                            right_index_address=right_index_address,
                            right_offset=right_offset,
                        )
                    # variable [?] variable
                    else:
                        right_value = right_symbol.get_symbol_value()
                        if task == "assignment":
                            if right_value == -1:
                                left_symbol.set_value(-1)
                            else:
                                left_symbol.set_value(right_value)

                        self.pass_task_to_machine(
                            task=task,
                            task_value=task_value,
                            loop_type=loop_type,
                            iterator_address=iterator_address,
                            left_symbol_address=left_symbol_address,
                            right_symbol_address=right_symbol_address,
                        )
                # variable [?] number
                else:
                    right_value = self.machine_values[1]
                    if task == "assignment":
                        left_symbol.set_value(right_value)

                    self.pass_task_to_machine(
                        task=task,
                        task_value=task_value,
                        loop_type=loop_type,
                        iterator_address=iterator_address,
                        left_symbol_address=left_symbol_address,
                        right_value=right_value,
                    )

            if not left_symbol.is_defined:
                left_symbol.is_defined = True
        else:
            if right_is_var:
                right_symbol = self.get_symbol_by_name(self.machine_values[1])
                right_symbol_address = right_symbol.get_address()
                left_value = self.machine_values[0]

                # number [?] tab(i)
                if right_symbol.is_tab:
                    right_index = self.tab_indexes.pop()
                    right_offset = -1

                    if right_index == -1:
                        right_index_address = self.get_symbol_by_name(
                            self.last_read_symbols.pop()
                        ).get_address()
                        right_offset = right_symbol.get_tab_offset()
                    else:
                        right_index_address = 0
                        right_symbol_address += (
                            right_index - right_symbol.get_tab_offset()
                        )

                    self.pass_task_to_machine(
                        task=task,
                        task_value=task_value,
                        loop_type=loop_type,
                        iterator_address=iterator_address,
                        left_value=left_value,
                        right_symbol_address=right_symbol_address,
                        right_index_address=right_index_address,
                        right_offset=right_offset,
                    )
                # number [?] variable
                else:
                    self.pass_task_to_machine(
                        task=task,
                        task_value=task_value,
                        loop_type=loop_type,
                        iterator_address=iterator_address,
                        left_value=left_value,
                        right_symbol_address=right_symbol_address,
                    )
            else:
                left_value = self.machine_values[0]
                right_value = self.machine_values[1]
                self.pass_task_to_machine(
                    task=task,
                    task_value=task_value,
                    loop_type=loop_type,
                    iterator_address=iterator_address,
                    left_value=left_value,
                    right_value=right_value,
                )

        self.machine_values = self.machine_values[2:]

    def get_symbol_by_name(self, pidentifier):
        for symbol in self.symbols:
            if pidentifier == symbol.get_pidentifier():
                return symbol

    def get_symbol_address(self, pidentifier, offset=0):
        symbol = self.get_symbol_by_name(pidentifier)

        if symbol.is_tab:
            return symbol.get_address() + offset
        else:
            return symbol.get_address()

    def pass_task_to_machine(
        self,
        task="",
        task_value="",
        loop_type="",
        iterator_address=-1,
        left_symbol_address=-1,
        left_value=-1,
        left_index_address=-1,
        left_offset=-1,
        right_symbol_address=-1,
        right_index_address=-1,
        right_value=-1,
        right_offset=-1,
    ):
        if task == "math_operation":
            self.machine_math_manager.carry_out_operation(
                operation=task_value,
                left_value=left_value,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_value=right_value,
                right_symbol_address=right_symbol_address,
                right_index_address=right_index_address,
                right_offset=right_offset,
            )
        elif task == "assignment":
            self.assignment_manager.carry_out_assignment(
                left_value=left_value,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_value=right_value,
                right_symbol_address=right_symbol_address,
                right_index_address=right_index_address,
                right_offset=right_offset,
            )
        elif task == "condition":
            self.machine_conditions_manager.carry_out_condition(
                condition=task_value,
                left_value=left_value,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_value=right_value,
                right_symbol_address=right_symbol_address,
                right_index_address=right_index_address,
                right_offset=right_offset,
            )
        elif task == "for_loop":
            self.code_generator.manage_for_loop(
                loop_type=loop_type,
                iterator_address=iterator_address,
                left_value=left_value,
                left_symbol_address=left_symbol_address,
                left_index_address=left_index_address,
                left_offset=left_offset,
                right_value=right_value,
                right_symbol_address=right_symbol_address,
                right_index_address=right_index_address,
                right_offset=right_offset,
            )

    def get_stacks(self):
        return self.tab_indexes, self.last_read_symbols, self.machine_values
