# project module


### project.formup(x)
handling the process of create new formula in the database
:param x: Formula object
:return: None


### project.ing(req_list_ing)
managing the process of getting new ingredient to the system
:param req_list_ing: list of characteristics required for the new ingredient
:return: none


### project.main()

### project.new(y, z)

* **Parameters**

    
    * **y** – list of characteristics needed for the creation of the desired item


    * **z** – the newly created item



* **Returns**

    None



### project.new_ing()

* **Returns**

    newly created ing object (out of existing data)



### project.new_phase(x)
creating the additional  requirements for the new created phase
:param x: is Phase class
:return: completed new phase object with its additional requirements


### project.update(x, y)
insert created ingredient to database
:param x: new ingredient (Ing object)
:param y: list of characteristics to update in the database
:return: None


### project.upload(x, r)

* **Parameters**

    
    * **x** – list pf existing ingredients


    * **r** – Name of ingredient user wants to add



* **Returns**

    updated list of ingredients for the current phase
