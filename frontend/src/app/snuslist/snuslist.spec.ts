import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Snuslist } from './snuslist';

describe('Snuslist', () => {
  let component: Snuslist;
  let fixture: ComponentFixture<Snuslist>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Snuslist]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Snuslist);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
