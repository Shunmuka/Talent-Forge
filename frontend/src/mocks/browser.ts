import { setupWorker } from 'msw';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
// TODO: initialize this worker before rendering pages locally.
