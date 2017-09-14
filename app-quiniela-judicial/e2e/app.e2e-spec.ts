import { QuinielaJudicialPage } from './app.po';

describe('quiniela-judicial App', () => {
  let page: QuinielaJudicialPage;

  beforeEach(() => {
    page = new QuinielaJudicialPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
