объект log надо сделать статическим 
 
 
 Создание /htaccess
     если надо перегенерировать нужно ввыключить/включить Friendly URL
     
     
Запуск XAMPP с наивысшим приоритетом
    https://remontka.pro/uac-disable-windows-10/

    Нет. Но есть такой способ обхода: создаем задание в планировщике заданий для выполнения этой программы с наивысшими правами, а потом создаем ярлык для запуска этого задания по имени:

    schtasks /run /tn "Имя задания"
    И он будет срабатывать без запроса UAC

           
                ###################################################
                
                        Supplier - класс поставщика

                ###################################################

        
        
        
        наследник от Driver, который расширяет возможности Селениум до мoих желаний


        Все классы поставщиков строятся на базе класса Supplier
        Каждый выполняет свой сценарий из файлов suppliers.<префикс поставщика>


        Инициализация класса конкретного поставщика товара:
        Supplier(lang = ['he','en','ru'] , supplier_name = <имя поставщика>) 


                    Ini()---------------+
                    |                   +---    path:Path
                    |                   |           физический адрес программы
                    |                   |           
                    |                   +---    path_str : str
                    |                   |           строка path
                    |                   |           
                    |                   +---    path_ini  : Path
                    |                   |           директория файлов иницилазации программы
                    |                   |           
                    |                   +---    path_ini_str : str
                    |                   |           строка path_ini
                    |                   |           
                    |                   +---    path_path_log_dir : Path
                    |                   |           директория файлов log
                    |                   |           
                    |                   +---    path_export_dir : Path
                    |                   |           директория файлов экспорта
                    |                   |           
                    |                   +---    start_time  : datetime
                    |                   +---    get_now(): datetime
                    |
                    |
                Log(Ini)----------------+
                |                       +---    header()
                |                       |           заголовок HTML лога в котором можно
                |                       |           прописать функции, например, jacascript
                |                       |           сейчас записана функция скрытия свойств
                |                       |           классов и типов в логе
                |                       |           
                |                       +---    screenshot(self , log = object) 
                |                       |
                |                       +---    print(self, log = object, prn_type="jupiter") 
                |                       |           |
                |                       |           \/
                |                       +---    write_log_to_file()
                |                       |
                |                       +---    logged(method_to_decorate)
                |                       +---    print_attr(self, *o):
                |
         Driver(Log)--------------------+
         |                              +---    driver : webdriver 
         |                              |
         |                              +---    current_url : str
         |                              |
         |                              +---    set_driver()
         |                              |
         |                              +---    driver_implicity_wait(self , wait)  --?
         |                              |
         |                              +---    wait(self , wait)                   --?
         |                              |
         |                              +---    wait_to_precence_located(self, locator) 
         |                              |
         |                              +---    wait_to_be_clickable(self, locator, time_to_wait = 5)
         |                              |
         |                              +---    get_url(self, url)
         |                              |
         |                              +---    click(self, locator)
         |                              |
         |                              +---    find(self, locator)
         |                              |
         |                              +---    get_elements_by_locator(self, locator)
         |                              |
         |                              +---    researh_elements(self, elements)
         |                              |
         |                              +---    page_refresh(self)
         |                              |
         |                              +---    close()
         |
Supplier(Driver)------------------------+---    run(self)
                                        |
                                        +---    export_to_csv(self,data)
                                        |
                                        +---    lang : str = attrib(kw_only = True)
                                        |           для какого языка собирается инфо  he, en, ru 
                                        |
                                        +---    supplier_name :str  = attrib(kw_only = True)                    
                                        |        имя поставщика     
                                        |
                                        +---    supplier_prefics :str  = attrib(init = False)
                                        |           префикс имени                             
                                        |
                                        +---    price_rule :str = attrib(init = False )                         
                                        |        пересчет цены от постащика для клиента              
                                        |
                                        +---    locators :json  =  attrib(init = False)                              
                                        |           локаторы элементов страницы                         
                                        |
                                        +---      start_url : str =  attrib(init = False)                              
                                        |          Начальный адрес сценария
                                        |
                                        +---       required_login : bool = attrib(init=False)      <--- вынести в сценарий           
                                        |
                                        +---    scenaries : list  =  attrib(init = False , factory = list)      
                                        |           Список сценариев
                                        |           
                                        +---    current_scenario :json = attrib(init = False)                   
                                        |               Текущий сценарий
                                        |           
                                        +---    current_scenario_category : str =  attrib(init=False)           
                                        |           Категория товаров по имени файла сценария
                                        |           
                                        +---    current_node  : str =  attrib(init=False)                       
                                        |          Исполняемый узел сценария
                                        |           
                                        +---    current_nodename  : str =  attrib(init=False)                   
                                        |           Имя испоняемого узла сценария
                                        |
                                        +---    required_login : bool
        

                            #################################################################################

                                                        Класс товара
   
                            #################################################################################

                    Ini()---------------+
                    |                   |
                    |                   +---    path:Path
                    |                   |           физический адрес программы
                    |                   |           
                    |                   +---    path_str : str
                    |                   |           строка path
                    |                   |           
                    |                   +---    path_ini  : Path
                    |                   |           директория файлов иницилазации программы
                    |                   |           
                    |                   +---    path_ini_str : str
                    |                   |           строка path_ini
                    |                   |           
                    |                   +---    path_path_log_dir : Path
                    |                   |           директория файлов log
                    |                   |           
                    |                   +---    path_export_dir : Path
                    |                   |           директория файлов экспорта
                    |                   |           
                    |                   +---    start_time  : datetime
                    |                   +---    get_now(): datetime
                    |
                    |
                Log(Ini)----------------+
                |                       |
                |                       +---    header()
                |                       |           заголовок HTML лога в котором можно
                |                       |           прописать функции, например, jacascript
                |                       |           сейчас записана функция скрытия свойств
                |                       |           классов и типов в логе
                |                       |           
                |                       +---    screenshot(self , log = object) 
                |                       |
                |                       +---    print(self, log = object, prn_type="jupiter") 
                |                       |       |
                |                       |       \/  
                |                       +---    write_log_to_file(self, log:object)
                |                       |
                |                       +---    logged(method_to_decorate)
                |                       +---    print_attr(self, *o):
                |
        Product(Log)--------------------+
                                        |
                                        +---