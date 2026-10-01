package cli

// Hidden acceptance tests for TASK-1, adapted from urfave/cli#2393 to use only the public API.

import (
	"bytes"
	"context"
	"errors"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestHiddenArgUsage(t *testing.T) {
	arg := &IntArg{Name: "ia"}
	require.Equal(t, "[ia]", arg.Usage())
	arg.Required = true
	require.Equal(t, "ia", arg.Usage())
	arg.UsageText = "foo-usage"
	require.Equal(t, "foo-usage", arg.Usage())
}

func TestHiddenSingleRequiredArg(t *testing.T) {
	tests := []struct {
		name                  string
		args                  []string
		argValue, exp, expErr string
	}{
		{name: "no args", args: []string{"foo"}, expErr: `Required argument "sa" not set`},
		{name: "no arg with def value", args: []string{"foo"}, argValue: "bar", expErr: `Required argument "sa" not set`},
		{name: "one arg", args: []string{"foo", "zbar"}, exp: "zbar"},
		{name: "empty string arg", args: []string{"foo", ""}, exp: ""},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			cmd := buildMinimalTestCommand()
			var s1 string
			cmd.Arguments = []Argument{&StringArg{Name: "sa", Value: test.argValue, Destination: &s1, Required: true}}
			err := cmd.Run(buildTestContext(t), test.args)
			if test.expErr != "" {
				require.EqualError(t, err, test.expErr)
				return
			}
			require.NoError(t, err)
			require.Equal(t, test.exp, s1)
		})
	}
}

func TestHiddenMissingRequiredArgDoesNotMutateValue(t *testing.T) {
	destination := "unchanged"
	arg := &StringArg{Name: "sa", Value: "default", Destination: &destination, Required: true}
	initialValue := arg.Get()
	writer, errWriter := &bytes.Buffer{}, &bytes.Buffer{}
	cmd := buildMinimalTestCommand()
	cmd.Writer, cmd.ErrWriter = writer, errWriter
	cmd.Arguments = []Argument{arg}
	err := cmd.Run(buildTestContext(t), []string{"foo"})
	require.Error(t, err)
	require.Equal(t, "unchanged", destination)
	require.Equal(t, initialValue, arg.Get())
	require.Contains(t, errWriter.String(), `Incorrect Usage: Required argument "sa" not set`)
	require.Contains(t, writer.String(), "NAME:")
}

func TestHiddenChainedRequiredArgs(t *testing.T) {
	cmd := buildMinimalTestCommand()
	cmd.Arguments = []Argument{&StringArg{Name: "first", Required: true}, &StringArg{Name: "second", Required: true}}
	require.EqualError(t, cmd.Run(buildTestContext(t), []string{"foo"}), `Required arguments "first, second" not set`)
	require.EqualError(t, cmd.Run(buildTestContext(t), []string{"foo", "one"}), `Required argument "second" not set`)
	require.NoError(t, cmd.Run(buildTestContext(t), []string{"foo", "one", "two"}))
}

func TestHiddenRequiredArgAfterOptionalArg(t *testing.T) {
	cmd := buildMinimalTestCommand()
	cmd.Arguments = []Argument{&StringArg{Name: "optional"}, &StringArg{Name: "required", Required: true}}
	require.EqualError(t, cmd.Run(buildTestContext(t), []string{"foo", "one"}), `Required argument "required" not set`)
	require.NoError(t, cmd.Run(buildTestContext(t), []string{"foo", "one", "two"}))
}

func TestHiddenRequiredArgAfterMultiValueArg(t *testing.T) {
	writer, errWriter := &bytes.Buffer{}, &bytes.Buffer{}
	cmd := buildMinimalTestCommand()
	cmd.Writer, cmd.ErrWriter = writer, errWriter
	cmd.Arguments = []Argument{&StringArgs{Name: "rest", Min: 0, Max: -1}, &StringArg{Name: "required", Required: true}}
	err := cmd.Run(buildTestContext(t), []string{"foo", "one", "two"})
	require.Error(t, err)
	require.Contains(t, errWriter.String(), `Incorrect Usage: Required argument "required" not set`)
	require.Contains(t, writer.String(), "NAME:")
}

func TestHiddenRequiredArgWithOnUsageError(t *testing.T) {
	expectedErr := errors.New("OnUsageError")
	var got error
	cmd := buildMinimalTestCommand()
	cmd.Arguments = []Argument{&StringArg{Name: "required", Required: true}}
	cmd.OnUsageError = func(_ context.Context, _ *Command, err error, _ bool) error {
		got = err
		return expectedErr
	}
	require.ErrorIs(t, cmd.Run(buildTestContext(t), []string{"foo"}), expectedErr)
	require.EqualError(t, got, `Required argument "required" not set`)
}

func TestHiddenArgumentRequiredUsageInCommandHelp(t *testing.T) {
	for _, test := range []struct {
		name     string
		required bool
		expected string
	}{
		{name: "optional", expected: "test run [options] [sa]"},
		{name: "required", required: true, expected: "test run [options] sa"},
	} {
		t.Run(test.name, func(t *testing.T) {
			output := &bytes.Buffer{}
			cmd := &Command{Name: "test", Writer: output, Commands: []*Command{
				{Name: "run", Arguments: []Argument{&StringArg{Name: "sa", Required: test.required}}},
			}}
			require.NoError(t, cmd.Run(buildTestContext(t), []string{"test", "run", "--help"}))
			require.Contains(t, output.String(), test.expected)
		})
	}
}
