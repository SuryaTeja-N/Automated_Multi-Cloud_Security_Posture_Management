const {Storage} = require('@google-cloud/storage');
const functions = require('@google-cloud/functions-framework');

const storage = new Storage();

functions.cloudEvent('remediate-gcp', async (cloudEvent) => {
    const file = cloudEvent.data;
    const bucketName = file.bucket;

    console.log(`Checking security settings for bucket: ${bucketName}`);

    try {
        // Get the current IAM policy
        const [policy] = await storage.bucket(bucketName).iam.getPolicy();

        // Remove all users with allUsers (public access)
        const filteredBindings = policy.bindings.filter(binding => !binding.members.includes("allUsers"));

        if (filteredBindings.length !== policy.bindings.length) {
            policy.bindings = filteredBindings;

            // Update the IAM policy
            await storage.bucket(bucketName).iam.setPolicy(policy);
            console.log(` Public access removed from bucket: ${bucketName}`);
        } else {
            console.log(` Bucket ${bucketName} is already secure.`);
        }
    } catch (error) {
        console.error(` Error securing bucket ${bucketName}:`, error);
    }
});
