import { realEstatePage, mountRealEstate } from './real-estate-ui.js';

const root=document.querySelector('#real-estate-root');
if(!root) throw new Error('real-estate-root missing');
root.innerHTML=realEstatePage();
mountRealEstate(root);
