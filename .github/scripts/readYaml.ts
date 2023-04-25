import * as yaml from 'yaml';
import * as fs from 'fs';
import yargs from 'yargs/yargs';
import { hideBin } from 'yargs/helpers';

interface Organization {
  name: string;
  owners: string[];
}

interface GitHubInstance {
  instance: string;
  url: string;
  organizations: Organization[];
}

interface InstanceList {
  github_instances: GitHubInstance[];
}

const readYamlFile = (filePath: string): InstanceList => {
  // Read the YAML file content
  const fileContent = fs.readFileSync(filePath, 'utf8');
  // Parse the YAML content and return the result
  return yaml.parse(fileContent) as InstanceList;
};

// Function to find an owner in the specified organization and GitHub instance
const findOwner = (
  instanceList: InstanceList,
  githubInstance: string,
  organizationName: string,
  username: string
) => {
  // Find the GitHub instance by name
  const instance = instanceList.github_instances.find(inst => inst.instance === githubInstance);
  if (!instance) return JSON.stringify(false);
  
  // Find the organization by name within the GitHub instance
  const organization = instance.organizations.find(org => org.name === organizationName);
  if (!organization) return JSON.stringify(false);
  
  // Check if the provided username is included in the organization's owners array
  if (organization.owners.includes(username)) {
    return JSON.stringify({
      instance: instance.instance,
      url: instance.url,
      name: organization.name,
      owner: username
    });
  } else {
    return JSON.stringify(false);
  }
};

// Read and parse the YAML file
const instanceList = readYamlFile('./github_instances.yaml');

// Parse command-line arguments using yargs
const argv = yargs(hideBin(process.argv))
  .option('github_instance', {
    alias: 'g',
    type: 'string',
    description: 'Name of the GitHub instance',
  })
  .option('organization', {
    alias: 'o',
    type: 'string',
    description: 'Name of the organization',
  })
  .option('user', {
    alias: 'u',
    type: 'string',
    description: 'Username to check',
  })
  .demandOption(['github_instance', 'organization', 'user'], 'Please provide GitHub instance, organization, and user arguments')
  .argv;
