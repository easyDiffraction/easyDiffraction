Feature: easyDiffraction set of BDD tests. part 1

    1. File load
    2. Structure visibility
    3. Chart visibility
    4. Fit button enabled

    Scenario: Structure/chart visibility
        Given Application is open
          And File is loaded

         When Structure tab open
         Then Structure should be visible


         When Chart tab open
         Then Chart should be visible

    Scenario: Parameters should be fittable
        Given Application is open
          And File is loaded

         When Fitting tab open
         And First parameter checked
         Then Fit button enabled
