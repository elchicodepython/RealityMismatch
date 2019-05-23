interface Translation {
  es: Array<i18n>;
  en: Array<i18n>;
  fr?: Array<i18n>;
  de?: Array<i18n>;
}

interface i18n {
  codename: string;
  text: string;
}
