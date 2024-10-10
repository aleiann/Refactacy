from flask import Blueprint, request, jsonify, Response
from cobol_to_ast import ASTGenerator
from llm import interagisci_con_gpt4
from cobol_append import get_full_cobol_code, get_dat_content
import json

import os
from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv('API_KEY')

cobolService = Blueprint('cobolService', __name__)


@cobolService.route('/getJavaCode', methods=['POST'])
def get_java_code():
    # Estrai il payload JSON dalla richiesta
    data = request.get_json()

    # Controlla se il payload è stato ricevuto correttamente
    if data is None:
         return jsonify({"error": "Invalid JSON"}), 400

    # dobbiamo avere anche owner, repo, path
    owner = data["owner"]
    repo = data["repo"]
    path = data["path"]

    full_cobol_code = get_full_cobol_code(owner=owner, repo=repo, path=path)

    # script che recupera tutti i file dat nella repo
    datContent = get_dat_content(owner, repo)

    # data deve essere già il main con tutte le concatenazioni
    ast = ASTGenerator(full_cobol_code)

    prompt = f'''Request for Java Code Generation from COBOL85 AST

Persona: COBOL to Java Translation Expert

Role: Act as an experienced software developer with advanced knowledge of both COBOL and Java. You specialize in
translating COBOL code, including handling complex constructs that may not have direct equivalents in Java, and
converting them optimally while adhering to Java programming conventions. Your task is to take an Abstract Syntax Tree
generated from COBOL85 code and transform it into Java code, preserving the original program’s logic and functionality.

Required Skills:
- Awareness of COBOL code structures and their corresponding translations in Java, allowing for proper explanation of how the Java code maps to the original COBOL logic.
- In-depth understanding of COBOL85 syntax and structures, including specific constructs like “PIC”, “PERFORM”, and “DIVISION”.
- Mastery of Java programming best practices, including naming conventions, exception handling, and structures like “try-catch”, methods, and classes.
- Ability to document the generated Java code with concise, explanatory comments in Italian, clearly explaining the translation of COBOL constructs.
- Capability to handle COBOL constructs that do not have a direct equivalent in Java, finding effective solutions and explaining them clearly in comments.
- Proficiency in generating documentation in JSON format, ensuring correct structure and consistent labeling of function names and descriptions.

AST Input:
{ast}'''+'''

Requirements:
Ensure that the Java code adheres to standard coding conventions.
Be careful to insert short comments in Italian language in the code to explain the functionality of each class field and each function.
If possible, handle any specific COBOL constructs that may not have a direct equivalent in Java.
Respond by providing me only the java code.
Remember to name the main function simply 'Main' and not 'MainProgram'.
Ensure that no content of any kind is generated before or after the template.

Here is an example of the input AST:
(startRule (compilationUnit (programUnit (identificationDivision IDENTIFICATION DIVISION .\n (programIdParagraph PROGRAM-ID .  (programName (cobolWord MAINPROGRAM)) .\n\n)) (environmentDivision ENVIRONMENT DIVISION .\n (environmentDivisionBody (inputOutputSection INPUT-OUTPUT SECTION .\n (inputOutputSectionParagraph (fileControlParagraph FILE-CONTROL .\n     (fileControlEntry (selectClause SELECT (fileName (cobolWord ACCOUNT-FILE))) (fileControlClause (assignClause ASSIGN TO (literal "contidb.dat"))) (fileControlClause (organizationClause ORGANIZATION IS LINE SEQUENTIAL))) .\n\n))))) (dataDivision DATA DIVISION .\n (dataDivisionSection (fileSection FILE SECTION .\n (fileDescriptionEntry FD (fileName (cobolWord ACCOUNT-FILE)) .\n\n))) (dataDivisionSection (workingStorageSection WORKING-STORAGE SECTION .\n (dataDescriptionEntry (dataDescriptionEntryFormat1 01 (dataName (cobolWord WS-USER-CHOICE)) (dataPictureClause PIC (pictureString (pictureChars X) (pictureChars () (pictureChars (integerLiteral 1)) (pictureChars )))) .\n)) (dataDescriptionEntry (dataDescriptionEntryFormat1 01 (dataName (cobolWord WS-ACCOUNT-NUMBER)) (dataPictureClause PIC (pictureString (pictureChars X) (pictureChars () (pictureChars (integerLiteral 10)) (pictureChars )))) .\n)) (dataDescriptionEntry (dataDescriptionEntryFormat1 01 (dataName (cobolWord WS-TRANSACTION-AMOUNT)) (dataPictureClause PIC (pictureString (pictureChars S9) (pictureChars () (pictureChars (integerLiteral 7)) (pictureChars )) (pictureChars V99))) .\n)) (dataDescriptionEntry (dataDescriptionEntryFormat1 01 (dataName (cobolWord WS-NEW-BALANCE)) (dataPictureClause PIC (pictureString (pictureChars S9) (pictureChars () (pictureChars (integerLiteral 7)) (pictureChars )) (pictureChars V99))) .\n\n)) (dataDescriptionEntry (dataDescriptionEntryFormat1 01 (dataName (cobolWord COMMAREA)) .\n    )) (dataDescriptionEntry (dataDescriptionEntryFormat1 05 (dataName (cobolWord CA-ACCOUNT-NUMBER)) (dataPictureClause PIC (pictureString (pictureChars X) (pictureChars () (pictureChars (integerLiteral 10)) (pictureChars )))) .\n    )) (dataDescriptionEntry (dataDescriptionEntryFormat1 05 (dataName (cobolWord CA-TRANSACTION-AMOUNT)) (dataPictureClause PIC (pictureString (pictureChars S9) (pictureChars () (pictureChars (integerLiteral 7)) (pictureChars )) (pictureChars V99))) .\n    )) (dataDescriptionEntry (dataDescriptionEntryFormat1 05 (dataName (cobolWord CA-NEW-BALANCE)) (dataPictureClause PIC (pictureString (pictureChars S9) (pictureChars () (pictureChars (integerLiteral 7)) (pictureChars )) (pictureChars V99))) .\n\n))))) (procedureDivision PROCEDURE DIVISION .\n\n     (procedureDivisionBody (paragraphs (paragraph (paragraphName (cobolWord MAIN-PARA)) .\n         (sentence (statement (displayStatement DISPLAY (displayOperand (literal "Benvenuto nel sistema bancario!")))) (statement (displayStatement DISPLAY (displayOperand (literal "1. Consulta il saldo")))) (statement (displayStatement DISPLAY (displayOperand (literal "2. Esegui una transazione (deposito/prelievo)")))) (statement (displayStatement DISPLAY (displayOperand (literal "Scegli l'operazione (1 o 2):")))) (statement (acceptStatement ACCEPT (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-USER-CHOICE))))))) (statement (ifStatement IF (condition (combinableCondition (simpleCondition (relationCondition (relationArithmeticComparison (arithmeticExpression (multDivs (powers (basis (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-USER-CHOICE))))))))) (relationalOperator =) (arithmeticExpression (multDivs (powers (basis (literal '1')))))))))) (ifThen (statement (performStatement PERFORM (performProcedureStatement (procedureName (paragraphName (cobolWord CONSULTA-SALDO))))))) (ifElse ELSE (statement (ifStatement IF (condition (combinableCondition (simpleCondition (relationCondition (relationArithmeticComparison (arithmeticExpression (multDivs (powers (basis (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-USER-CHOICE))))))))) (relationalOperator =) (arithmeticExpression (multDivs (powers (basis (literal '2')))))))))) (ifThen (statement (performStatement PERFORM (performProcedureStatement (procedureName (paragraphName (cobolWord TRANSAZIONE))))))) (ifElse ELSE (statement (displayStatement DISPLAY (displayOperand (literal "Scelta non valida"))))) END-IF))))) .\n\n        ) (sentence (statement (stopStatement STOP RUN)) .\n\n    )) (paragraph (paragraphName (cobolWord CONSULTA-SALDO)) .\n         (sentence (statement (displayStatement DISPLAY (displayOperand (literal "Inserisci il numero del conto:")))) (statement (acceptStatement ACCEPT (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-ACCOUNT-NUMBER))))))) (statement (moveStatement MOVE (moveToStatement (moveToSendingArea (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-ACCOUNT-NUMBER)))))) TO (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord CA-ACCOUNT-NUMBER)))))))) (statement (callStatement CALL (literal 'BALANCEMODULE') (callUsingPhrase USING (callUsingParameter (callByReferencePhrase (callByReference (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord COMMAREA))))))))))) (statement (displayStatement DISPLAY (displayOperand (literal "Il saldo corrente del conto ")) (displayOperand (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-ACCOUNT-NUMBER)))))) (displayOperand (literal " è: ")) (displayOperand (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord CA-NEW-BALANCE)))))))) .\n\n    )) (paragraph (paragraphName (cobolWord TRANSAZIONE)) .\n         (sentence (statement (displayStatement DISPLAY (displayOperand (literal "Inserisci il numero del conto:")))) (statement (acceptStatement ACCEPT (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-ACCOUNT-NUMBER))))))) (statement (displayStatement DISPLAY (displayOperand (literal "Inserisci l'importo della transazione (positivo per depositi, negativo per prelievi):")))) (statement (acceptStatement ACCEPT (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-TRANSACTION-AMOUNT))))))) (statement (moveStatement MOVE (moveToStatement (moveToSendingArea (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-ACCOUNT-NUMBER)))))) TO (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord CA-ACCOUNT-NUMBER)))))))) (statement (moveStatement MOVE (moveToStatement (moveToSendingArea (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-TRANSACTION-AMOUNT)))))) TO (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord CA-TRANSACTION-AMOUNT)))))))) (statement (callStatement CALL (literal 'TRANSACTIONMODULE') (callUsingPhrase USING (callUsingParameter (callByReferencePhrase (callByReference (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord COMMAREA))))))))))) (statement (displayStatement DISPLAY (displayOperand (literal "Il saldo aggiornato del conto ")) (displayOperand (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord WS-ACCOUNT-NUMBER)))))) (displayOperand (literal " è: ")) (displayOperand (identifier (qualifiedDataName (qualifiedDataNameFormat1 (dataName (cobolWord CA-NEW-BALANCE)))))))) .\n))))))) <EOF>)
Here is an example of the code you might generate for me:

import java.io.*;\nimport java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n\n        System.out.println(\"Benvenuto nel sistema bancario!\");\n        System.out.println(\"1. Consulta il saldo\");\n        System.out.println(\"2. Esegui una transazione (deposito/prelievo)\");\n        System.out.println(\"Scegli l'operazione (1 o 2):\");\n        String userChoice = scanner.nextLine();\n\n        if (\"1\".equals(userChoice)) {\n            consultaSaldo(scanner);\n        } else if (\"2\".equals(userChoice)) {\n            eseguiTransazione(scanner);\n        } else {\n            System.out.println(\"Scelta non valida\");\n        }\n    }\n\n    private static void consultaSaldo(Scanner scanner) {\n        System.out.println(\"Inserisci il numero del conto:\");\n        String accountNumber = scanner.nextLine();\n\n        BalanceModule balanceModule = new BalanceModule();\n        double balance = balanceModule.getBalance(accountNumber);\n\n        System.out.println(\"Il saldo corrente del conto \" + accountNumber + \" è: \" + balance);\n    }\n\n    private static void eseguiTransazione(Scanner scanner) {\n        System.out.println(\"Inserisci il numero del conto:\");\n        String accountNumber = scanner.nextLine();\n\n        System.out.println(\"Inserisci l'importo della transazione (positivo per depositi, negativo per prelievi):\");\n        double transactionAmount = scanner.nextDouble();\n\n        TransactionModule transactionModule = new TransactionModule();\n        double updatedBalance = transactionModule.updateBalance(accountNumber, transactionAmount);\n\n        System.out.println(\"Il saldo aggiornato del conto \" + accountNumber + \" è: \" + updatedBalance);\n    }\n}\n\nclass BalanceModule {\n    public double getBalance(String accountNumber) {\n        try (BufferedReader reader = new BufferedReader(new FileReader(\"contidb.dat\"))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                String[] fields = line.split(\",\");\n                if (fields[0].trim().equals(accountNumber)) {\n                    return Double.parseDouble(fields[1]);\n                }\n            }\n        } catch (IOException e) {\n            e.printStackTrace();\n        }\n        System.out.println(\"Conto non trovato.\");\n        return 0.0;\n    }\n}\n\nclass TransactionModule {\n    public double updateBalance(String accountNumber, double transactionAmount) {\n        File inputFile = new File(\"contidb.dat\");\n        File tempFile = new File(\"temp.dat\");\n\n        try (BufferedReader reader = new BufferedReader(new FileReader(inputFile));\n             BufferedWriter writer = new BufferedWriter(new FileWriter(tempFile))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                String[] fields = line.split(\",\");\n                if (fields[0].trim().equals(accountNumber)) {\n                    double newBalance = Double.parseDouble(fields[1]) + transactionAmount;\n                    writer.write(accountNumber + \",\" + newBalance + \"\\n\");\n                    return newBalance;\n                } else {\n                    writer.write(line + \"\\n\");\n                }\n            }\n        } catch (IOException e) {\n            e.printStackTrace();\n        }\n\n        if (!inputFile.delete() || !tempFile.renameTo(inputFile)) {\n            System.out.println(\"Errore nell'aggiornamento del file.\");\n        }\n\n        System.out.println(\"Conto non trovato.\");\n        return 0.0;\n    }\n}

For this project, the .dat files are the following :''' + f'''
{datContent}''' + '''
Be careful with the name of the .dat files, especially whether they are written in lowercase or uppercase, and with the separators between each value within the line.
If the name is lowercase, you must report it as lowercase in the java code, while if the name is uppercase, you must report it as uppercase.
Moreover, if the values within the line are many spaces, consider to split the values by these spaces.


Also consider whether the answer is clear and easy for the target audience to understand.
Think not only about the output, but also about the context of the request.
At the end of the process, review the entire response, identify any errors, and generate the response correctly.
Avoid including false or invented information in your answer.
Check if the answer contains internal contradictions or if there are aspects that are inconsistent with the rest of the answer.
Reflect on your answer again after making any changes.
    '''
    json_string = interagisci_con_gpt4(APIKEY=APIKEY, prompt=prompt)


    json_string = json_string.replace("`", "")

    return json_string, 200

@cobolService.route('/getDoc', methods=['POST'])
def get_java_doc():
    # Estrai il payload JSON dalla richiesta
    payload = request.get_json()
    code = payload["javaCode"]
    #
    # # Controlla se il payload è stato ricevuto correttamente
    if code is None:
         return jsonify({"error": "Invalid JSON"}), 400

    prompt = f'''
    Request for Code Documentation Generation from given Java code

Persona: Java Code Documentation Specialist

Role: You are an experienced software engineer with expertise in Java programming and a strong focus on technical documentation.
Your primary responsibility is to analyze Java code, understand its structure, functionality, and purpose, and generate
clear, accurate, and detailed documentation. This documentation will include descriptions of classes, methods, inputs,
outputs, and the overall functionality of the code. You are proficient in writing documentation that is both technical
and user-friendly, catering to developers and non-developers alike.

Required skills:
- Ability to produce clear, concise, and well-structured documentation that explains complex code functionalities in an accessible manner.
- Strong knowledge of Java programming, enabling accurate and detailed documentation of methods, classes, and their functionality.
- Ability to write concise, informative comments in Italian, detailing the purpose and functionality of specific code segments.
- Proficiency in generating documentation in JSON format, ensuring correct structure and consistent labeling of function names and descriptions.
- Ability to provide documentation and comments in Italian.

JAVA Input:
{code} '''+'''

Requirements:
Ensure that the generated documentation adheres to standard documentation conventions.
The documentation need to have specific terms that adheres the best practive of the Java language.
Provide an explanation of up to 500 characters of the generated Java code and its correspondence to the
original COBOL85 code.
Respond by providing me only a JSON in the following format:
{
    "descriptionCode": "the description up to 500 characters",
    "documentation": [
        {
            "nameFunction": "the name of the function",
            "descriptionFunction": "long-medium explanation of the function for documentation"
        },
        {
            "nameFunction": "the name of the function",
            "descriptionFunction": "long-medium explanation of the function for documentation"
        }, ...
    ]
}
Ensure that the JSON response is fully populated with the general description of the code and function descriptions.
Ensure that the JSON response structure is maintained.
Ensure that no content of any kind is generated before or after the template.


Replace all placeholders:
- 'up to 500 characters explanation' with the description that you generate based on the code content,
- for each function in the java code that you have generated replace 'function name' with the name of the function (the
same of the method sign) and 'explanation of the function for documentation' with the explanation of that function
specifyng what it takes in input, what it do and the output, explaining the operation that the function do.

Here is an example of the input Java code:
import java.io.*;\nimport java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n\n        // Messaggi di benvenuto e scelta dell'operazione\n        System.out.println(\"Benvenuto nel sistema bancario!\");\n        System.out.println(\"1. Consulta il saldo\");\n        System.out.println(\"2. Esegui una transazione (deposito/prelievo)\");\n        System.out.println(\"Scegli l'operazione (1 o 2):\");\n        String userChoice = scanner.nextLine();\n\n        // Esegue l'operazione in base alla scelta dell'utente\n        if (\"1\".equals(userChoice)) {\n            consultaSaldo(scanner);\n        } else if (\"2\".equals(userChoice)) {\n            eseguiTransazione(scanner);\n        } else {\n            System.out.println(\"Scelta non valida\");\n        }\n    }\n\n    // Funzione per consultare il saldo\n    private static void consultaSaldo(Scanner scanner) {\n        System.out.println(\"Inserisci il numero del conto:\");\n        String accountNumber = scanner.nextLine();\n\n        BalanceModule balanceModule = new BalanceModule();\n        double balance = balanceModule.getBalance(accountNumber);\n\n        System.out.println(\"Il saldo corrente del conto \" + accountNumber + \" è: \" + balance);\n    }\n\n    // Funzione per eseguire una transazione\n    private static void eseguiTransazione(Scanner scanner) {\n        System.out.println(\"Inserisci il numero del conto:\");\n        String accountNumber = scanner.nextLine();\n\n        System.out.println(\"Inserisci l'importo della transazione (positivo per depositi, negativo per prelievi):\");\n        double transactionAmount = scanner.nextDouble();\n        scanner.nextLine(); // Consuma la linea residua\n\n        TransactionModule transactionModule = new TransactionModule();\n        double updatedBalance = transactionModule.updateBalance(accountNumber, transactionAmount);\n\n        System.out.println(\"Il saldo aggiornato del conto \" + accountNumber + \" è: \" + updatedBalance);\n    }\n}\n\nclass BalanceModule {\n    // Funzione per ottenere il saldo del conto\n    public double getBalance(String accountNumber) {\n        try (BufferedReader reader = new BufferedReader(new FileReader(\"CONTIDB.DAT\"))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                String[] fields = line.split(\",\");\n                if (fields[0].trim().equals(accountNumber)) {\n                    return Double.parseDouble(fields[1]);\n                }\n            }\n        } catch (IOException e) {\n            e.printStackTrace();\n        }\n        System.out.println(\"Conto non trovato.\");\n        return 0.0;\n    }\n}\n\nclass TransactionModule {\n    // Funzione per aggiornare il saldo del conto\n    public double updateBalance(String accountNumber, double transactionAmount) {\n        File inputFile = new File(\"CONTIDB.DAT\");\n        File tempFile = new File(\"temp.dat\");\n\n        try (BufferedReader reader = new BufferedReader(new FileReader(inputFile));\n             BufferedWriter writer = new BufferedWriter(new FileWriter(tempFile))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                String[] fields = line.split(\",\");\n                if (fields[0].trim().equals(accountNumber)) {\n                    double newBalance = Double.parseDouble(fields[1]) + transactionAmount;\n                    writer.write(accountNumber + \",\" + newBalance + \"\\n\");\n                    return newBalance;\n                } else {\n                    writer.write(line + \"\\n\");\n                }\n            }\n        } catch (IOException e) {\n            e.printStackTrace();\n        }\n\n        if (!inputFile.delete() || !tempFile.renameTo(inputFile)) {\n            System.out.println(\"Errore nell'aggiornamento del file.\");\n        }\n\n        System.out.println(\"Conto non trovato.\");\n        return 0.0;\n    }\n}\n
Here is an example of the output you might generate for me:
{
    "descriptionCode": "Il codice Java simula il comportamento del programma COBOL85. La classe Main gestisce l'interazione con l'utente e chiama i moduli BalanceModule e TransactionModule per operazioni specifiche. BalanceModule legge il saldo di un conto, mentre TransactionModule aggiorna il saldo dopo una transazione.",
    "documentation": [
        {
            "nameFunction": "main",
            "descriptionFunction": "La funzione main avvia il programma, mostra il menu principale e gestisce l'input dell'utente per scegliere tra consultare il saldo o eseguire una transazione. Non ha parametri di input e non restituisce alcun valore.",
            "parameters": [
                "parameter1": "descrizione del parametro 1",
                "parameter2": "descrizione del parametro 2"
            ]
        },
        {
            "nameFunction": "consultaSaldo",
            "descriptionFunction": "Questa funzione richiede all'utente il numero del conto e chiama il modulo BalanceModule per ottenere il saldo del conto. Stampa il saldo corrente del conto. Parametro di input: Scanner per leggere l'input dell'utente. Non restituisce alcun valore.",
            "parameters": [
                "parameter1": "descrizione del parametro 1",
                "parameter2": "descrizione del parametro 2"
            ]
        },
        {
            "nameFunction": "eseguiTransazione",
            "descriptionFunction": "Questa funzione richiede all'utente il numero del conto e l'importo della transazione, quindi chiama il modulo TransactionModule per aggiornare il saldo del conto. Stampa il saldo aggiornato. Parametro di input: Scanner per leggere l'input dell'utente. Non restituisce alcun valore.",
            "parameters": [
                "parameter1": "descrizione del parametro 1",
                "parameter2": "descrizione del parametro 2"
            ]
        },
        {
            "nameFunction": "getBalance",
            "descriptionFunction": "Questa funzione del modulo BalanceModule legge il file dei conti e restituisce il saldo del conto specificato. Parametro di input: String accountNumber. Restituisce il saldo del conto come double.",
            "parameters": [
                "parameter1": "descrizione del parametro 1",
                "parameter2": "descrizione del parametro 2"
            ]
        },
        {
            "nameFunction": "updateBalance",
            "descriptionFunction": "Questa funzione del modulo TransactionModule legge il file dei conti, aggiorna il saldo del conto con l'importo della transazione e scrive i dati aggiornati in un file temporaneo. Parametri di input: String accountNumber, double transactionAmount. Restituisce il nuovo saldo del conto come double.",
            "parameters": [
                "parameter1": "descrizione del parametro 1",
                "parameter2": "descrizione del parametro 2"
            ]
        }
    ]
}

Also consider whether the answer is clear and easy for the target audience to understand.
Think not only about the output, but also about the context of the request.
At the end of the process, review the entire response, identify any errors, and generate the response correctly.
Avoid including false or invented information in your answer.
Check if the answer contains internal contradictions or if there are aspects that are inconsistent with the rest of the answer.
Reflect on your answer again after making any changes.
          
            
            
    '''


    json_string = interagisci_con_gpt4(APIKEY=APIKEY, prompt=prompt)

    json_string = json_string.replace("`", "")

    print(json_string)

    # Trova l'indice del primo '{'
    brace_index = json_string.find('{')
    if brace_index != -1:
        json_string = json_string[brace_index:]

    print(json_string)

    json = jsonify(json_string)

    return json_string, 200
