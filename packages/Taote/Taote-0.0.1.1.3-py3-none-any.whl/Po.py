
def describe_dict(df, x):
  
    """ df = DataFrame
        x = sum, mean, count, std, max, min, median, mode or null
    Se crea un diccionario Clave (Nombre Columna): Valor (medida descriptiva deseada)
    
    Creat a code dictionary (Column name):Value (desired descriptive measure)

    Ejemplo:  describe_dict(DataFrame,'sum')
        describe_dict(DataFrame,'null')['Columna'] = Nulos

    --------------------------------------------------------------------------------------------------   

    """

    if x == 'sum':
        return {i: df[i].sum()  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}
    elif x == 'mean':
        return {i: df[i].mean()  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}
    elif x == 'count':
        return {i: df[i].count()  for i in list(df.columns)}
    elif x == 'std':
        return {i: df[i].std()  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}
    elif x == 'max':
        return {i: df[i].max()  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}
    elif x == 'min':
        return {i: df[i].min()  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}
    elif x == 'median':
        return {i: df[i].median()  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}
    elif x == 'null':
        return {i: df[i].isnull().sum()  for i in list(df.columns)} 
    elif x == 'mode':
        return {i: df[i].mode()[0]  for i in list(df.columns) if df.dtypes[i] == float or df.dtypes[i] == int}

    
   
def snake(df, n=5):
  """ df = DataFrame
       n = número filas aleatorias, por defecto 5
  Imprime un DataFrame de 15 filas: head + sample + tail
    Se puede alterar el número de filas aleatorias (sample, por defecto 5)

    n= Random row number, 5 by default
    Print a dataframe of 15 rows:head + sample + tail
    The number of random rows can be altered (sample by default 5)

    Ejemplo: snake(df)
             snake(df, n=8)
  --------------------------------------------------------------------------------------------------   
     
  """    
  import pandas as pd
  return pd.concat([df.head(), df.sample(n), df.tail()])



def cast_int_notdecimal(df):
  """ df = DataFrame 
     Convertir columnas de un DataFrame float a int si no tiene decimales
    Esta función utiliza el módulo math para obtener la parte decimal de un número
    Pasamos como parámetro un dataframe, crea un diccionario con la suma de los valores por columna
    Y extrae el valor decimal de la suma, si es 0.0, convierte esa columna a int
    Se puede utilizar aún teniendo nulos las columna
    
    Convert columns from a dataframe float to int if it has not got decimals
    This function uses the math module to obtain the decimal part of the number
    We forward a dataframe as a parameter, create a dictionary with the sum of the values per column
    And extract the decimal value of the sum, if it is 0.0, Convert that column to int
    It can be used even having the column as nule
    --------------------------------------------------------------------------------------------------   
     
    """

  from  math import modf
  import pandas as pd
  
  lista = [i for i in list(df.columns) if df.dtypes[i] == float  ]
  dicc = {i: df[i].sum() for i in lista}
  for i,j in dicc.items():
    parte_decimal, parte_entera = modf(j)
    
    
    if parte_decimal == 0.0:
      
        if df[i].isnull().sum() != 0:
            df[i] = pd.merge(df[i].dropna().astype(int),df[i])
            df[i] = pd.merge(df[i].dropna().astype(int),df[i])
        else:
            df[i] = df[i].astype(int)
        print(f"Pasamos a entero {i.upper()} porque no tiene decimales, suma total: {j}".center(110,'='))


def clean_html(df,x):
    """ df = DataFrame
         x = Columna
  Función útil para Preparación de Datos en NLP
  Limpia etiquetas HTML

    Gadget for preparation of NLP data
    Clean HTML labels

  importa re
  Ejemplo:
      df['columna']=df['columna'].apply(clean_html)
  --------------------------------------------------------------------------------------------------   
     
  """
    def clean_html(text):
        import re
        import pandas as pd
        clean = re.compile('<.*?>')
        return re.sub(clean, '',text)
    df[x]=df[x].apply(clean_html)
    

def remove_special(df,x):
    """
        df = DataFrame
         x = Columna
  Función útil para Preparación de Datos en NLP
  Elimina carácteres especiales
  
    Gadget tfor preparation of NLP data
    Eliminates special symbols


  Ejemplo:
      df['columna']=df['columna'].apply(remove_special)
  --------------------------------------------------------------------------------------------------   
     
  """
    def remove_special(text):
        x=''
        for i in text:
            if i.isalnum():
                x=x+i
            else:
                x=x+' '
        return x
    df[x]=df[x].apply(remove_special)
    

def rendundant_words(df,x, language):
    """
        df = DataFrame
         x = Columna
         language = 'idioma'
  Función útil para Preparación de Datos en NLP
  Elimina palabras no significativas del idioma utilizado
  Ejemplo:
      rendundant_words(DataFrame,'Column', 'english') 
  Utiliza  stopwords de nltk.corpus
  Hay que tener instalado nltk
  Utilizar nltk.download()

  Gadget for preparation of NLP data
    Delete spcial symbols
    Use stopwords of nltk.corpus
    nltk must be installed
    Use nltk.download()
--------------------------------------------------------------------------------------------------   
     
  """
    from nltk.corpus import stopwords
    df[x] = [i for i in df[x].str.split() if i not in stopwords.words(language)]





def suffixes(df,x):
    from nltk.stem.porter import PorterStemmer
    ps= PorterStemmer()
    df[x] = [ps.stem(i)  for i in df[x]]


    """
        df = DataFrame
         x = Columna
    Función útil para Preparación de Datos en NLP
    Elimina sufijos de una columna
    Hay que tener instalado PorterStemmer
    Utiliza PorterStemmer de nltk.stem.porter
        Ejemplo: suffixes(DataFrame,'column') 


     Gadget for preparation of NLP data
    Deletes suffix from a column
    PorterSteammer must be installed
    Use PorterStemmer de nltk.stem.porter
  --------------------------------------------------------------------------------------------------   
      
    """




def isfloat(n):
    """
    n = string
    Función para aplicar a Strings
    Devuelve True si el String es 'float'
    Ejemplo: '4.0' , '255445.0', '65597.2659'
        Devuelve False para '4.00'

    Gadget to apply to strings
    Return true if the String is ‘float’
--------------------------------------------------------------------------------------------------   
         
    """
    try:
        if  (float(n)%1 !=0) or (n[-2] =='.'):
            return True
        else:
            return False
    except:
        return False



def Taylor_exp(n,x):
    """
    Calcula la serie de taylor de e^x pasando como parámetro
        n = número interacciones
        x = valor
    Utiliza la funcion math.factorial y itertools.accumulate
    
    Calculate Taylor series of e`x procceding as a parameter
    n= number of interactions
    x=value
    Use the function math.factorial and itertools.accumulate

--------------------------------------------------------------------------------------------------   
     
    """
    from math import factorial
    from itertools import accumulate
    exp = list(accumulate([(x**i/factorial(i)) for i in range(n)]))
    while exp[-1]  == exp[-2]:
        [exp.pop() for i in exp  if exp[-1] == exp[-2]]
    return exp






def RTaylor_exp(n,x):
    """
    Calcula el error relativo la serie de taylor de e^x pasando como parámetro
        n = número interacciones
        x = valor
    Utiliza la funcion math.factorial y itertools.accumulate


    Calculate the relative error the Taylor series of e`x proceeding as a parameter 
    n= number of interactions
    x= value
    Use the function math.factorial and iterpools.accumulate
--------------------------------------------------------------------------------------------------   
     
    """
    from math import factorial
    from itertools import accumulate
    try:
        exp = list(accumulate([(x**i/factorial(i)) for i in range(n)])) # Más rápdio
        exp =[0] + list([abs((j-(exp[1:][i-1]))/j) for i,j in enumerate(exp[1:])])
    
        while  exp[-1]  == exp[-3]:
            [exp.pop() for i in exp  if exp[-1] == exp[-2]]
        return exp
    except:
        print("Se produce el error ErrorDivisionZero")





def TaylorSerie_exp(x,taylor =1, Error_Rel = 0,prnt=0): 
    """
    x = valor
    taylor = Serie de Taylor exp^x
    Error_Rel = Error relativo Serie de Taylor
    prnt = imprimir porceso

        Calcula la serie de taylor de e^x por defecto 
                Ejemplo: Taylor_exp(0.99)
        Calcula el la serie de errores relativos si se añade valor 0
                Ejemplo: Taylor_exp(0.99,0)
        Imprime todo el proceso para prnt=1
                Ejemplo: Taylor_exp(0.99,prnt=1)
        Utiliza la funcion math.factorial y itertools.accumulate


    x = value
    taylor = Taylor Series exp^x
    Erros_Rel = ERelative error Taylor series
    prnt=print process
    Calculate Taylor series of e^x by default
    Calculate the series of relative errors if value 0 is added
    Print the complete process for prnt=1
    Use the function math.factorial and itertools.accumulate
--------------------------------------------------------------------------------------------------   
     
    """
    from math import factorial
    from itertools import accumulate
    from numpy import exp
    try:
        n=3       # Hay que empezar en n=3
        exp = list(accumulate([(x**i/factorial(i)) for i in range(n)])) # Más rápdio
        e_R = [0]+list([abs((j-(exp[1:][i-1]))/j) for i,j in enumerate(exp[1:])])
        while e_R[-1]  != 0:
            n+=1
            exp = list(accumulate([(x**i/factorial(i)) for i in range(n)])) 
        
            e_R = list([abs((j-(exp[1:][i-1]))/j) for i,j in enumerate(exp[1:])])
        
           
            if len(e_R)>6:      # Cuando los 3 últimos valores se repite, se para la iteración
                if e_R[-1] == e_R[-3]:
                    print("Se repiten los últimos 3 valores, así que paramos la interacción")
                    break

        e_R = [0] +e_R   # Añadimos el Error Relativo correspondiente a la primera iteración
    
        if prnt == True:
            print(f"""

     0. Para x = {x}
     1. Se han necesitado {len(exp)} interacciones para que el Error Relativo entre dos iteraciones sea menor a 1𝑒−8 
     2. Valor aproximado exp^x = {exp[-1]} 
     3. Error Relativo ={e_R[-1]}
""") 
            print("{:<10} {:>25} {:>25} \n{}".format(
            "n", "exp^X", "Valor Relativo", "-" * 62))
            for j,k in enumerate(dict(zip(exp,e_R))):
        
                print("{:<10} {:>25} {:>25}".format(j+1, k, dict(zip(exp,e_R))[k]))
            print(f"\nValor Exacto exp^{x} = {exp(x)}")
        if taylor == 1:
            return exp   
        else:
            return e_R
    except:
        print("Se produce el error ErrorDivisionZero")



