import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISplashScreen, Dialog } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { LabIcon } from '@jupyterlab/ui-components';
import { Throttler } from '@lumino/polling';
import { DisposableDelegate } from '@lumino/disposable';
import stxSvgstrFull from '../style/systemathics-logo-full.svg';
import stxSvgstrSquares from '../style/systemathics-logo-squares.svg';

export const stxIconFull = new LabIcon({
  name: 'stxlogofull',
  svgstr: stxSvgstrFull
});

export const stxIconSquares = new LabIcon({
  name: 'stxlogosquares',
  svgstr: stxSvgstrSquares
});

/**
 * Initialization data for the ganymede-logo extension.
 */
const logo: JupyterFrontEndPlugin<void> = {
  id: 'ganymede-logo',
  autoStart: true,
  requires: [ILabShell],
  activate: (app: JupyterFrontEnd, shell: ILabShell) => {
    console.log('ganymede-logo activated');
    const logo = new Widget();
    stxIconSquares.element({
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

/**
 * The command IDs used by the apputils plugin.
 */
namespace CommandIDs {
  export const reset = 'apputils:reset';
}

/**
 * The interval in milliseconds before recover options appear during splash.
 */
const SPLASH_RECOVER_TIMEOUT = 12000;

/**
 * Initialization data for the ganymede-splashscreen extension.
 */
const splash: JupyterFrontEndPlugin<ISplashScreen> = {
  id: 'ganymede-splashscreen:plugin',
  autoStart: true,
  provides: ISplashScreen,
  activate: (app: JupyterFrontEnd) => {
    const { commands, restored } = app;
    console.log('JupyterLab extension ganymede-splashscreen is activated!');
    // Return ISplashScreen.
    const splash = document.createElement('div');
    stxIconFull.element({
      container: splash,
      position: 'fixed',
      top: '50%',
      left: '50%',
      right: '-50%',
      height: 'auto',
      width: '10%',
      transform: 'translate(-50%, -50%)'
      //animation: 'rotation 4s infinite linear'
      //animation: 'beat .7s infinite alternate'
    });
    splash.id = 'stx-splash';

    // Create debounced recovery dialog function.
    let dialog: Dialog<unknown> | null;
    const recovery = new Throttler(
      async () => {
        if (dialog) {
          return;
        }

        dialog = new Dialog({
          title: 'Loading...',
          body: `The loading screen is taking a long time. 
Would you like to clear the workspace or keep waiting?`,
          buttons: [
            Dialog.cancelButton({ label: 'Keep Waiting' }),
            Dialog.warnButton({ label: 'Clear Workspace' })
          ]
        });

        try {
          const result = await dialog.launch();
          dialog.dispose();
          dialog = null;
          if (result.button.accept && commands.hasCommand(CommandIDs.reset)) {
            return commands.execute(CommandIDs.reset);
          }

          // Re-invoke the recovery timer in the next frame.
          requestAnimationFrame(() => {
            // Because recovery can be stopped, handle invocation rejection.
            void recovery.invoke().catch(_ => undefined);
          });
        } catch (error) {
          /* no-op */
        }
      },
      { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' }
    );

    // Return ISplashScreen.
    let splashCount = 0;
    return {
      show: () => {
        splash.classList.remove('splash-fade');
        splashCount++;
        console.log('adding');
        document.body.appendChild(splash);

        // Because recovery can be stopped, handle invocation rejection.
        void recovery.invoke().catch(_ => undefined);

        return new DisposableDelegate(async () => {
          await restored;
          if (--splashCount === 0) {
            void recovery.stop();

            if (dialog) {
              dialog.dispose();
              dialog = null;
            }

            splash.classList.add('splash-fade');
            window.setTimeout(() => {
              document.body.removeChild(splash);
            }, 200);
          }
        });
      }
    };
  }
};
/**
 * Export the plugins as default.
 */
const plugins: JupyterFrontEndPlugin<any>[] = [logo, splash];

export default plugins;
