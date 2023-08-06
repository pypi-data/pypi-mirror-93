import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { Widget } from '@lumino/widgets';
import { LabIcon } from '@jupyterlab/ui-components';
import stxSvgstr from '../style/systemathics-logo-squares.svg';

export const stxIcon = new LabIcon({
  name: 'barpkg:foo',
  svgstr: stxSvgstr
});

/**
 * Initialization data for the ganymede-logo extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'ganymede-logo',
  autoStart: true,
  requires: [ILabShell],
  activate: (app: JupyterFrontEnd, shell: ILabShell) => {
    console.log('ganymede-logo activated');
    const logo = new Widget();
    stxIcon.element({
      container: logo.node,
      elementPosition: 'center',
      margin: '2px 2px 2px 8px',
      height: 'auto',
      width: '16px'
    });
    logo.id = 'stx-MainLogo';
    shell
      .widgets('top')
      .next()
      .setHidden(true);
    shell.add(logo, 'top', { rank: 0 });
  }
};

export default extension;
