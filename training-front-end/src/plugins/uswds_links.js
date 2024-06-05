/*
 * The purpose of this is to apply the appropriate class to links
 * it will add uswds usa-link--external for non gsa.gov links
 */
import {selectAll} from 'hast-util-select';

export function processLinksPlugin() {
    return function (node) {
      selectAll('a', node).forEach(node => {
        const properties = node.properties
        properties.className = 'usa-link'

        let domain;
        try {
          domain = new URL(properties.href)
        } catch(e) {
          // Exceptions will be raised with relative links
          // these will all be local, so ignore
          return
        }

        if (!(domain.hostname === 'gsa.gov' || domain.hostname === 'www.gsa.gov'|| domain.protocol === 'mailto:')) {
          properties.className += ' usa-link--external'
        }

      });
    } 
}