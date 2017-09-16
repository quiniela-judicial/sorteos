import { AppQuinielaJudicialPage } from './app.po';

describe('app-quiniela-judicial App', () => {
  let page: AppQuinielaJudicialPage;

  beforeEach(() => {
    page = new AppQuinielaJudicialPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
