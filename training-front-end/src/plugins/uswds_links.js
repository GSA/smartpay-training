/*
 * The purpose of this is to apply the appropriate class to links
 * it will add uswds usa-link--external for non gsa.gov links
 */
import selector from 'hast-util-select';

const { selectAll } = selector;

export default () => {
    return node => selectAll('a', node).forEach(node => {
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
    
      const internalHosts = [
        'www.gsa.gov',
        'smartpay.gsa.gov',
        'training.smartpay.gsa.gov'
      ];

      if (!internalHosts.includes(domain.hostname)){
        properties.className += ' usa-link--external'
      }
    
    });
};

