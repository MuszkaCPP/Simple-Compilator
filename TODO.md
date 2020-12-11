## **code_generator:**

##### **Optymalizacja**:
- przy store_variable:
    - jesli current_value * 2^(x) == var_a --> robimy x/2 razy SHL, zamiast x razy INC
        