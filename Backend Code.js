<script>
  function runPythonScript(scriptName, args, callback) {
    const formData = new FormData();
    formData.append('scriptName', scriptName);
    formData.append('args', JSON.stringify(args));
    fetch('run_script.py', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(callback);
  }

  // Example usage:
  const scriptName = 'importre1.py';
  const args = ['arg1', 'arg2', 'arg3'];
  runPythonScript(scriptName, args, output => {
    console.log(output);
  });
</script>


Python Script Connectivity:

import sys

def main(args):
    # Your code here
    result = 0
    for arg in args:
        result += int(arg)
    return str(result)

if __name__ == '__main__':
    args = sys.argv[1:]
    print(main(args))





