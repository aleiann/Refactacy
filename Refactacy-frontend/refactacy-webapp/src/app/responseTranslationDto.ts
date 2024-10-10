import { Documentation, JavaCodeObject } from "./responseTranslationObject";


export class JavaCodeClass implements JavaCodeObject {
    javaCode: string;
    descriptionCode: string;
    documentation: Documentation[];
  
    constructor(
      javaCode: string,
      descriptionCode: string,
      documentation: Documentation[]
    ) {
      this.javaCode = javaCode;
      this.descriptionCode = descriptionCode;
      this.documentation = documentation;
    }
  }
  