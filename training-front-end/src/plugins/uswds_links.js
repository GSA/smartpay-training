/*
 * The purpose of this is to apply the appropriate class to links
 * it will add uswds usa-link--external for non gsa.gov links
 */
import selector from 'hast-util-select';

const { selectAll } = selector;

export default () => {
    return node => selectAll('a', node).forEach(node => {
      const properties = node.properties
      let domain = new URL(properties.href)

      if (domain.hostname.endsWith('smartpay-training')) {
        properties.className = 'usa-link'
      } else {
        properties.className = 'usa-link usa-link--external'
      }
    });
};

