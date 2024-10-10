
export interface Documentation {
    nameFunction: string;
    descriptionFunction: string;
  }
  
  // Definisci l'interfaccia per l'oggetto principale
  export interface JavaCodeObject {
    javaCode: string;
    descriptionCode: string;
    documentation: Documentation[];
  }
  